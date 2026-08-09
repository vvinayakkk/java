package com.bookstore.config;

import com.bookstore.entity.Author;
import com.bookstore.entity.Book;
import com.bookstore.entity.Category;
import com.bookstore.repository.AuthorRepository;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.CategoryRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * Seeds demo data so list/search/available endpoints are measurable from Day 1.
 */
@Component
public class DataLoader implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataLoader.class);

    private final AuthorRepository authorRepository;
    private final CategoryRepository categoryRepository;
    private final BookRepository bookRepository;

    public DataLoader(AuthorRepository authorRepository,
                      CategoryRepository categoryRepository,
                      BookRepository bookRepository) {
        this.authorRepository = authorRepository;
        this.categoryRepository = categoryRepository;
        this.bookRepository = bookRepository;
    }

    @Override
    public void run(String... args) {
        if (bookRepository.count() > 0) {
            log.info("Database already seeded ({} books). Skipping DataLoader.", bookRepository.count());
            return;
        }

        List<Author> authors = seedAuthors();
        List<Category> categories = seedCategories();
        int bookCount = seedBooks(authors, categories);

        log.info("Seeded {} authors, {} categories, {} books",
                authors.size(), categories.size(), bookCount);
    }

    private List<Author> seedAuthors() {
        String[][] data = {
                {"Ada Lovelace", "Mathematician and early computing pioneer."},
                {"Grace Hopper", "Computer scientist and COBOL pioneer."},
                {"Alan Turing", "Foundational work in computation and cryptography."},
                {"Donald Knuth", "Author of The Art of Computer Programming."},
                {"Barbara Liskov", "Programming methodology and distributed systems."}
        };

        List<Author> authors = new ArrayList<>();
        for (String[] row : data) {
            Author author = new Author();
            author.setName(row[0]);
            author.setBiography(row[1]);
            authors.add(authorRepository.save(author));
        }
        return authors;
    }

    private List<Category> seedCategories() {
        String[][] data = {
                {"Software Engineering", "Design, architecture, and delivery practices."},
                {"Algorithms", "Problem-solving and computational thinking."},
                {"Distributed Systems", "Reliability, scale, and consistency."},
                {"Security", "Threat modeling and secure coding."},
                {"Career", "Engineering judgment and professional growth."}
        };

        List<Category> categories = new ArrayList<>();
        for (String[] row : data) {
            Category category = new Category();
            category.setName(row[0]);
            category.setDescription(row[1]);
            categories.add(categoryRepository.save(category));
        }
        return categories;
    }

    private int seedBooks(List<Author> authors, List<Category> categories) {
        String[] titleWords = {
                "Patterns", "Systems", "Reliability", "Refactoring", "Concurrency",
                "Observability", "Architecture", "Testing", "Performance", "Design",
                "APIs", "Caching", "Messaging", "Incidents", "Delivery"
        };

        List<Book> books = new ArrayList<>();
        for (int i = 1; i <= 90; i++) {
            Book book = new Book();
            String word = titleWords[(i - 1) % titleWords.length];
            book.setTitle(word + " Handbook Vol. " + i);
            book.setIsbn(String.format("978-0-%04d-%04d-%d", i, 1000 + i, i % 10));
            book.setPrice(BigDecimal.valueOf(9.99 + (i % 40)).setScale(2, RoundingMode.HALF_UP));
            // Every 10th book is out of stock for /available contrast
            book.setStockQuantity(i % 10 == 0 ? 0 : (i % 25) + 1);
            book.setDescription("Seeded book for residency labs: " + word.toLowerCase() + " topics.");
            book.setPublicationDate(LocalDate.of(2000 + (i % 25), (i % 12) + 1, (i % 28) + 1));
            book.setAuthor(authors.get((i - 1) % authors.size()));
            book.setCategory(categories.get((i - 1) % categories.size()));
            books.add(book);
        }

        return bookRepository.saveAll(books).size();
    }
}
