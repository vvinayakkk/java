package com.bookstore.service;

import com.bookstore.dto.BookDTO;
import com.bookstore.dto.BookPageResponse;
import com.bookstore.entity.Author;
import com.bookstore.entity.Book;
import com.bookstore.entity.Category;
import com.bookstore.exception.ResourceNotFoundException;
import com.bookstore.repository.AuthorRepository;
import com.bookstore.repository.BookRepository;
import com.bookstore.repository.CategoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class BookService {

    private static final int MAX_PAGE_SIZE = 50;

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private AuthorRepository authorRepository;

    @Autowired
    private CategoryRepository categoryRepository;

    @Autowired
    private CatalogSyncService catalogSyncService;

    @Value("${app.catalog-sync.async:true}")
    private boolean catalogSyncAsync;

    public BookPageResponse getAllBooks(int page, int size, String sortBy, String sortDir) {
        int safePage = Math.max(page, 0);
        int safeSize = size < 1 ? 10 : Math.min(size, MAX_PAGE_SIZE);
        String safeSortBy = (sortBy == null || sortBy.isBlank()) ? "id" : sortBy;
        String safeSortDir = (sortDir == null || sortDir.isBlank()) ? "asc" : sortDir;

        Sort sort = safeSortDir.equalsIgnoreCase("desc")
                ? Sort.by(safeSortBy).descending()
                : Sort.by(safeSortBy).ascending();
        Pageable pageable = PageRequest.of(safePage, safeSize, sort);
        Page<Book> result = bookRepository.findAll(pageable);

        List<BookDTO> content = result.getContent().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());

        return new BookPageResponse(
                content,
                result.getNumber(),
                result.getSize(),
                result.getTotalElements(),
                result.getTotalPages(),
                safeSortBy,
                safeSortDir
        );
    }

    @Cacheable(cacheNames = "books", key = "#id")
    @Transactional(readOnly = true)
    public BookDTO getBookById(Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));
        return convertToDTO(book);
    }

    public BookDTO getBookByIsbn(String isbn) {
        Book book = bookRepository.findByIsbn(isbn)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with ISBN: " + isbn));
        return convertToDTO(book);
    }

    public List<BookDTO> searchBooksByTitle(String title) {
        return bookRepository.findByTitleContainingIgnoreCase(title).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public List<BookDTO> getBooksByAuthor(Long authorId) {
        return bookRepository.findByAuthorId(authorId).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public List<BookDTO> getBooksByCategory(Long categoryId) {
        return bookRepository.findByCategoryId(categoryId).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public List<BookDTO> getBooksByPriceRange(BigDecimal minPrice, BigDecimal maxPrice) {
        return bookRepository.findByPriceRange(minPrice, maxPrice).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public List<BookDTO> getAvailableBooks() {
        return bookRepository.findAvailableBooks().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    @CacheEvict(cacheNames = "books", allEntries = true)
    public BookDTO createBook(BookDTO bookDTO) {
        if (bookRepository.findByIsbn(bookDTO.getIsbn()).isPresent()) {
            throw new IllegalArgumentException("Book with ISBN " + bookDTO.getIsbn() + " already exists");
        }

        Book book = convertToEntity(bookDTO);
        Book savedBook = bookRepository.save(book);

        if (catalogSyncAsync) {
            catalogSyncService.syncAfterCreateAsync(savedBook);
        } else {
            catalogSyncService.syncAfterCreate(savedBook);
        }

        return convertToDTO(savedBook);
    }

    @CacheEvict(cacheNames = "books", key = "#id")
    public BookDTO updateBook(Long id, BookDTO bookDTO) {
        Book existingBook = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));

        if (!existingBook.getIsbn().equals(bookDTO.getIsbn())) {
            if (bookRepository.findByIsbn(bookDTO.getIsbn()).isPresent()) {
                throw new IllegalArgumentException("Book with ISBN " + bookDTO.getIsbn() + " already exists");
            }
        }

        updateBookEntity(existingBook, bookDTO);
        Book updatedBook = bookRepository.save(existingBook);
        return convertToDTO(updatedBook);
    }

    @CacheEvict(cacheNames = "books", key = "#id")
    public void deleteBook(Long id) {
        if (!bookRepository.existsById(id)) {
            throw new ResourceNotFoundException("Book not found with id: " + id);
        }
        bookRepository.deleteById(id);
    }

    private BookDTO convertToDTO(Book book) {
        BookDTO dto = new BookDTO();
        dto.setId(book.getId());
        dto.setTitle(book.getTitle());
        dto.setIsbn(book.getIsbn());
        dto.setPrice(book.getPrice());
        dto.setStockQuantity(book.getStockQuantity());
        dto.setDescription(book.getDescription());
        dto.setPublicationDate(book.getPublicationDate());
        dto.setAuthorId(book.getAuthor().getId());
        dto.setCategoryId(book.getCategory().getId());
        dto.setAuthorName(book.getAuthor().getName());
        dto.setCategoryName(book.getCategory().getName());
        return dto;
    }

    private Book convertToEntity(BookDTO bookDTO) {
        Book book = new Book();
        book.setTitle(bookDTO.getTitle());
        book.setIsbn(bookDTO.getIsbn());
        book.setPrice(bookDTO.getPrice());
        book.setStockQuantity(bookDTO.getStockQuantity() != null ? bookDTO.getStockQuantity() : 0);
        book.setDescription(bookDTO.getDescription());
        book.setPublicationDate(bookDTO.getPublicationDate());

        Author author = authorRepository.findById(bookDTO.getAuthorId())
                .orElseThrow(() -> new ResourceNotFoundException("Author not found with id: " + bookDTO.getAuthorId()));
        book.setAuthor(author);

        Category category = categoryRepository.findById(bookDTO.getCategoryId())
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + bookDTO.getCategoryId()));
        book.setCategory(category);

        return book;
    }

    private void updateBookEntity(Book book, BookDTO bookDTO) {
        book.setTitle(bookDTO.getTitle());
        book.setIsbn(bookDTO.getIsbn());
        book.setPrice(bookDTO.getPrice());
        book.setStockQuantity(bookDTO.getStockQuantity() != null ? bookDTO.getStockQuantity() : 0);
        book.setDescription(bookDTO.getDescription());
        book.setPublicationDate(bookDTO.getPublicationDate());

        if (!book.getAuthor().getId().equals(bookDTO.getAuthorId())) {
            Author author = authorRepository.findById(bookDTO.getAuthorId())
                    .orElseThrow(() -> new ResourceNotFoundException("Author not found with id: " + bookDTO.getAuthorId()));
            book.setAuthor(author);
        }

        if (!book.getCategory().getId().equals(bookDTO.getCategoryId())) {
            Category category = categoryRepository.findById(bookDTO.getCategoryId())
                    .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + bookDTO.getCategoryId()));
            book.setCategory(category);
        }
    }
}
