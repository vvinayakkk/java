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
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.test.util.ReflectionTestUtils;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @Mock
    private AuthorRepository authorRepository;

    @Mock
    private CategoryRepository categoryRepository;

    @Mock
    private CatalogSyncService catalogSyncService;

    @InjectMocks
    private BookService bookService;

    private Author author;
    private Category category;
    private Book book;
    private BookDTO bookDTO;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(bookService, "catalogSyncAsync", true);

        author = new Author();
        author.setId(1L);
        author.setName("J.K. Rowling");
        author.setBiography("British author");

        category = new Category();
        category.setId(1L);
        category.setName("Fantasy");
        category.setDescription("Fantasy fiction");

        book = new Book();
        book.setId(1L);
        book.setTitle("Harry Potter");
        book.setIsbn("978-0747532699");
        book.setPrice(new BigDecimal("29.99"));
        book.setStockQuantity(50);
        book.setDescription("A fantasy novel");
        book.setPublicationDate(LocalDate.of(1997, 6, 26));
        book.setAuthor(author);
        book.setCategory(category);

        bookDTO = new BookDTO();
        bookDTO.setId(1L);
        bookDTO.setTitle("Harry Potter");
        bookDTO.setIsbn("978-0747532699");
        bookDTO.setPrice(new BigDecimal("29.99"));
        bookDTO.setStockQuantity(50);
        bookDTO.setDescription("A fantasy novel");
        bookDTO.setPublicationDate(LocalDate.of(1997, 6, 26));
        bookDTO.setAuthorId(1L);
        bookDTO.setCategoryId(1L);
    }

    @Test
    void testGetAllBooks() {
        Page<Book> page = new PageImpl<>(Arrays.asList(book));
        when(bookRepository.findAll(any(Pageable.class))).thenReturn(page);

        BookPageResponse result = bookService.getAllBooks(0, 10, "id", "asc");

        assertNotNull(result);
        assertEquals(1, result.getContent().size());
        assertEquals("Harry Potter", result.getContent().get(0).getTitle());
        assertEquals(1, result.getTotalElements());
        verify(bookRepository, times(1)).findAll(any(Pageable.class));
    }

    @Test
    void testGetBookById_Success() {
        // Given
        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));

        // When
        BookDTO result = bookService.getBookById(1L);

        // Then
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("Harry Potter", result.getTitle());
        assertEquals("978-0747532699", result.getIsbn());
        verify(bookRepository, times(1)).findById(1L);
    }

    @Test
    void testGetBookById_NotFound() {
        // Given
        when(bookRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> bookService.getBookById(1L));
        verify(bookRepository, times(1)).findById(1L);
    }

    @Test
    void testGetBookByIsbn_Success() {
        // Given
        when(bookRepository.findByIsbn("978-0747532699")).thenReturn(Optional.of(book));

        // When
        BookDTO result = bookService.getBookByIsbn("978-0747532699");

        // Then
        assertNotNull(result);
        assertEquals("978-0747532699", result.getIsbn());
        verify(bookRepository, times(1)).findByIsbn("978-0747532699");
    }

    @Test
    void testGetBookByIsbn_NotFound() {
        // Given
        when(bookRepository.findByIsbn("invalid-isbn")).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> bookService.getBookByIsbn("invalid-isbn"));
        verify(bookRepository, times(1)).findByIsbn("invalid-isbn");
    }

    @Test
    void testSearchBooksByTitle() {
        // Given
        List<Book> books = Arrays.asList(book);
        when(bookRepository.findByTitleContainingIgnoreCase("Harry")).thenReturn(books);

        // When
        List<BookDTO> result = bookService.searchBooksByTitle("Harry");

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("Harry Potter", result.get(0).getTitle());
        verify(bookRepository, times(1)).findByTitleContainingIgnoreCase("Harry");
    }

    @Test
    void testCreateBook_Success() {
        // Given
        when(bookRepository.findByIsbn(bookDTO.getIsbn())).thenReturn(Optional.empty());
        when(authorRepository.findById(1L)).thenReturn(Optional.of(author));
        when(categoryRepository.findById(1L)).thenReturn(Optional.of(category));
        when(bookRepository.save(any(Book.class))).thenReturn(book);

        // When
        BookDTO result = bookService.createBook(bookDTO);

        // Then
        assertNotNull(result);
        assertEquals("Harry Potter", result.getTitle());
        verify(bookRepository, times(1)).findByIsbn(bookDTO.getIsbn());
        verify(authorRepository, times(1)).findById(1L);
        verify(categoryRepository, times(1)).findById(1L);
        verify(bookRepository, times(1)).save(any(Book.class));
        verify(catalogSyncService, times(1)).syncAfterCreateAsync(any(Book.class));
        verify(catalogSyncService, never()).syncAfterCreate(any(Book.class));
    }

    @Test
    void testCreateBook_DuplicateIsbn() {
        // Given
        when(bookRepository.findByIsbn(bookDTO.getIsbn())).thenReturn(Optional.of(book));

        // When & Then
        assertThrows(IllegalArgumentException.class, () -> bookService.createBook(bookDTO));
        verify(bookRepository, times(1)).findByIsbn(bookDTO.getIsbn());
        verify(bookRepository, never()).save(any(Book.class));
    }

    @Test
    void testCreateBook_AuthorNotFound() {
        // Given
        when(bookRepository.findByIsbn(bookDTO.getIsbn())).thenReturn(Optional.empty());
        when(authorRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> bookService.createBook(bookDTO));
        verify(authorRepository, times(1)).findById(1L);
        verify(bookRepository, never()).save(any(Book.class));
    }

    @Test
    void testUpdateBook_Success() {
        // Given
        BookDTO updatedDTO = new BookDTO();
        updatedDTO.setTitle("Updated Title");
        updatedDTO.setIsbn("978-0747532699");
        updatedDTO.setPrice(new BigDecimal("39.99"));
        updatedDTO.setStockQuantity(100);
        updatedDTO.setAuthorId(1L);
        updatedDTO.setCategoryId(1L);

        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
        when(bookRepository.save(any(Book.class))).thenReturn(book);

        // When
        BookDTO result = bookService.updateBook(1L, updatedDTO);

        // Then
        assertNotNull(result);
        verify(bookRepository, times(1)).findById(1L);
        verify(bookRepository, times(1)).save(any(Book.class));
    }

    @Test
    void testUpdateBook_NotFound() {
        // Given
        when(bookRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> bookService.updateBook(1L, bookDTO));
        verify(bookRepository, times(1)).findById(1L);
        verify(bookRepository, never()).save(any(Book.class));
    }

    @Test
    void testDeleteBook_Success() {
        // Given
        when(bookRepository.existsById(1L)).thenReturn(true);
        doNothing().when(bookRepository).deleteById(1L);

        // When
        bookService.deleteBook(1L);

        // Then
        verify(bookRepository, times(1)).existsById(1L);
        verify(bookRepository, times(1)).deleteById(1L);
    }

    @Test
    void testDeleteBook_NotFound() {
        // Given
        when(bookRepository.existsById(1L)).thenReturn(false);

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> bookService.deleteBook(1L));
        verify(bookRepository, times(1)).existsById(1L);
        verify(bookRepository, never()).deleteById(anyLong());
    }

    @Test
    void testGetBooksByAuthor() {
        // Given
        List<Book> books = Arrays.asList(book);
        when(bookRepository.findByAuthorId(1L)).thenReturn(books);

        // When
        List<BookDTO> result = bookService.getBooksByAuthor(1L);

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        verify(bookRepository, times(1)).findByAuthorId(1L);
    }

    @Test
    void testGetBooksByCategory() {
        // Given
        List<Book> books = Arrays.asList(book);
        when(bookRepository.findByCategoryId(1L)).thenReturn(books);

        // When
        List<BookDTO> result = bookService.getBooksByCategory(1L);

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        verify(bookRepository, times(1)).findByCategoryId(1L);
    }

    @Test
    void testGetAvailableBooks() {
        // Given
        List<Book> books = Arrays.asList(book);
        when(bookRepository.findAvailableBooks()).thenReturn(books);

        // When
        List<BookDTO> result = bookService.getAvailableBooks();

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        verify(bookRepository, times(1)).findAvailableBooks();
    }
}

