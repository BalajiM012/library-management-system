const { dbHelpers } = require('../src/lib/db')
const bcrypt = require('bcryptjs')

async function seedDatabase() {
  try {
    console.log('Starting database initialization...')

    // Create admin user
    const adminPassword = await bcrypt.hash('admin123', 10)
    await dbHelpers.createUser('admin', adminPassword, 'admin')
    console.log('Created admin user')

    // Create sample student users
    const studentPassword = await bcrypt.hash('student123', 10)
    await dbHelpers.createUser('student1', studentPassword, 'student')
    await dbHelpers.createUser('student2', studentPassword, 'student')
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
      await dbHelpers.createBook(
        book.title,
        book.author,
        book.isbn,
        book.copies
      )
    }
    console.log('Created sample books')

    // Create sample loans
    const student1 = await dbHelpers.getUserByUsername('student1')
    const book1 = await dbHelpers.query('SELECT id FROM books LIMIT 1')
    
    if (student1 && book1.rows[0]) {
      const dueDate = new Date()
      dueDate.setDate(dueDate.getDate() + 14)
      
      await dbHelpers.createLoan(student1.id, book1.rows[0].id, dueDate)
      await dbHelpers.updateBookAvailability(book1.rows[0].id, false)
      console.log('Created sample loan')
    }

    console.log('Database initialization completed successfully!')
  } catch (error) {
    console.error('Error initializing database:', error)
    process.exit(1)
  }
}

// Initialize database schema and seed data
async function initializeDatabase() {
  try {
    await dbHelpers.query('BEGIN')
    
    // Initialize schema first
    await dbHelpers.initializeDatabase()
    console.log('Database schema created')

    // Seed data
    await seedDatabase()
    
    await dbHelpers.query('COMMIT')
    console.log('All database operations completed successfully!')
  } catch (error) {
    await dbHelpers.query('ROLLBACK')
    console.error('Database initialization failed:', error)
    process.exit(1)
  }
}

// Run initialization
initializeDatabase()
