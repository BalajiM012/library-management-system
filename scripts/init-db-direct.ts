import { Pool } from 'pg'
import bcrypt from 'bcryptjs'

// Database connection configuration
// Wait for database to be ready
const waitForDb = async (retries = 15, delay = 2000) => {
  for (let i = 0; i < retries; i++) {
    try {
      console.log('Attempting to connect to database...')
      const testPool = new Pool({
        user: 'postgres',
        password: 'postgres',
        host: 'postgres_db',
        port: 5432,
        database: 'postgres'
      })
      
      console.log('Pool created, testing connection...')
      const result = await testPool.query('SELECT 1')
      console.log('Connection test successful:', result.rows)
      await testPool.end()
      return true
    } catch (err) {
      console.error(`Connection attempt ${i + 1}/${retries} failed:`, err)
      if (i < retries - 1) {
        console.log(`Waiting ${delay}ms before next attempt...`)
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }
  throw new Error('Could not connect to database after multiple attempts')
}

const pool = new Pool({
  user: 'postgres',
  password: 'postgres',
  host: 'postgres_db',
  port: 5432,
  database: 'library_db'
})

// Helper function to execute queries
async function query(text: string, params?: any[]) {
  const client = await pool.connect()
  try {
    const result = await client.query(text, params)
    return result
  } finally {
    client.release()
  }
}

async function initializeDatabase() {
  const createTablesQuery = `
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(255) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'student')),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Books table
    CREATE TABLE IF NOT EXISTS books (
      id SERIAL PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      author VARCHAR(255) NOT NULL,
      isbn VARCHAR(13) UNIQUE,
      total_copies INTEGER NOT NULL DEFAULT 1,
      available_copies INTEGER NOT NULL DEFAULT 1,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Loans table
    CREATE TABLE IF NOT EXISTS loans (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id),
      book_id INTEGER REFERENCES books(id),
      borrowed_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      due_date TIMESTAMP WITH TIME ZONE NOT NULL,
      returned_date TIMESTAMP WITH TIME ZONE,
      fine_amount DECIMAL(10,2) DEFAULT 0,
      status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'returned', 'overdue')),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Book Categories table
    CREATE TABLE IF NOT EXISTS categories (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL UNIQUE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Book-Category relationship table
    CREATE TABLE IF NOT EXISTS book_categories (
      book_id INTEGER REFERENCES books(id),
      category_id INTEGER REFERENCES categories(id),
      PRIMARY KEY (book_id, category_id)
    );
  `

  try {
    await query(createTablesQuery)
    console.log('Database schema initialized successfully')
  } catch (error) {
    console.error('Error initializing database schema:', error)
    throw error
  }
}

async function seedDatabase() {
  try {
    console.log('Starting database initialization...')

    // Create admin user
    const adminPassword = await bcrypt.hash('admin123', 10)
    await query(
      'INSERT INTO users (username, password, role) VALUES ($1, $2, $3) ON CONFLICT (username) DO NOTHING',
      ['admin', adminPassword, 'admin']
    )
    console.log('Created admin user')

    // Create sample student users
    const studentPassword = await bcrypt.hash('student123', 10)
    await query(
      'INSERT INTO users (username, password, role) VALUES ($1, $2, $3), ($4, $5, $6) ON CONFLICT (username) DO NOTHING',
      ['student1', studentPassword, 'student', 'student2', studentPassword, 'student']
    )
    console.log('Created sample student users')

    // Create sample books
    const books = [
      {
        title: 'The Great Gatsby',
        author: 'F. Scott Fitzgerald',
        isbn: '9780743273565',
        copies: 3
      },
      {
        title: 'To Kill a Mockingbird',
        author: 'Harper Lee',
        isbn: '9780446310789',
        copies: 5
      },
      {
        title: '1984',
        author: 'George Orwell',
        isbn: '9780451524935',
        copies: 4
      },
      {
        title: 'Pride and Prejudice',
        author: 'Jane Austen',
        isbn: '9780141439518',
        copies: 3
      },
      {
        title: 'The Catcher in the Rye',
        author: 'J.D. Salinger',
        isbn: '9780316769488',
        copies: 2
      }
    ]

    for (const book of books) {
      await query(
        'INSERT INTO books (title, author, isbn, total_copies, available_copies) VALUES ($1, $2, $3, $4, $4) ON CONFLICT (isbn) DO NOTHING',
        [book.title, book.author, book.isbn, book.copies]
      )
    }
    console.log('Created sample books')

    console.log('Database initialization completed successfully!')
  } catch (error) {
    console.error('Error initializing database:', error)
    process.exit(1)
  } finally {
    await pool.end()
  }
}

// Run initialization
async function main() {
  try {
    console.log('Waiting for database to be ready...')
    await waitForDb()
    
    // Create database if it doesn't exist
    const pgPool = new Pool({
      user: 'postgres',
      password: 'postgres',
      host: 'postgres_db',
      port: 5432,
      database: 'postgres'
    })
    
    try {
      await pgPool.query('CREATE DATABASE library_db')
      console.log('Created library_db database')
    } catch (err: any) {
      if (err.code === '42P04') {
        console.log('library_db database already exists')
      } else {
        throw err
      }
    } finally {
      await pgPool.end()
    }

    console.log('Initializing database schema...')
    await initializeDatabase()
    console.log('Seeding database...')
    await seedDatabase()
  } catch (error) {
    console.error('Database setup failed:', error)
    process.exit(1)
  }
}

main()
