package com.bookstore.controller;

import com.bookstore.dto.BookDTO;
import com.bookstore.dto.BookPageResponse;
import com.bookstore.service.BookService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.bookstore.exception.GlobalExceptionHandler;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class BookControllerTest {

    private MockMvc mockMvc;

    @Mock
    private BookService bookService;

    @InjectMocks
    private BookController bookController;

    private ObjectMapper objectMapper;

    private BookDTO bookDTO;

    @BeforeEach
    void setUp() {
        objectMapper = new ObjectMapper();
        objectMapper.findAndRegisterModules();
        mockMvc = MockMvcBuilders.standaloneSetup(bookController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setMessageConverters(new MappingJackson2HttpMessageConverter(objectMapper))
                .build();

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
        bookDTO.setAuthorName("J.K. Rowling");
        bookDTO.setCategoryName("Fantasy");
    }

    @Test
    void testGetAllBooks() throws Exception {
        BookPageResponse page = new BookPageResponse(
                Arrays.asList(bookDTO), 0, 10, 1, 1, "id", "asc");
        when(bookService.getAllBooks(0, 10, "id", "asc")).thenReturn(page);

        mockMvc.perform(get("/api/books"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.content[0].id").value(1L))
                .andExpect(jsonPath("$.content[0].title").value("Harry Potter"))
                .andExpect(jsonPath("$.totalElements").value(1));

        verify(bookService, times(1)).getAllBooks(0, 10, "id", "asc");
    }

    @Test
    void testGetBookById() throws Exception {
        // Given
        when(bookService.getBookById(1L)).thenReturn(bookDTO);

        // When & Then
        mockMvc.perform(get("/api/books/1"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.title").value("Harry Potter"));

        verify(bookService, times(1)).getBookById(1L);
    }

    @Test
    void testGetBookByIsbn() throws Exception {
        // Given
        when(bookService.getBookByIsbn("978-0747532699")).thenReturn(bookDTO);

        // When & Then
        mockMvc.perform(get("/api/books/isbn/978-0747532699"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.isbn").value("978-0747532699"));

        verify(bookService, times(1)).getBookByIsbn("978-0747532699");
    }

    @Test
    void testSearchBooksByTitle() throws Exception {
        // Given
        List<BookDTO> books = Arrays.asList(bookDTO);
        when(bookService.searchBooksByTitle("Harry")).thenReturn(books);

        // When & Then
        mockMvc.perform(get("/api/books/search")
                        .param("title", "Harry"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("Harry Potter"));

        verify(bookService, times(1)).searchBooksByTitle("Harry");
    }

    @Test
    void testCreateBook() throws Exception {
        // Given
        BookDTO newBookDTO = new BookDTO();
        newBookDTO.setTitle("New Book");
        newBookDTO.setIsbn("978-1234567890");
        newBookDTO.setPrice(new BigDecimal("19.99"));
        newBookDTO.setStockQuantity(30);
        newBookDTO.setAuthorId(1L);
        newBookDTO.setCategoryId(1L);

        when(bookService.createBook(any(BookDTO.class))).thenReturn(bookDTO);

        // When & Then
        mockMvc.perform(post("/api/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(newBookDTO)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1L));

        verify(bookService, times(1)).createBook(any(BookDTO.class));
    }

    @Test
    void testCreateBook_InvalidInput() throws Exception {
        // Given - Missing required fields
        BookDTO invalidBookDTO = new BookDTO();
        invalidBookDTO.setTitle(""); // Empty title should fail validation

        // When & Then
        mockMvc.perform(post("/api/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidBookDTO)))
                .andExpect(status().isBadRequest());

        verify(bookService, never()).createBook(any(BookDTO.class));
    }

    @Test
    void testUpdateBook() throws Exception {
        // Given
        BookDTO updatedDTO = new BookDTO();
        updatedDTO.setTitle("Updated Title");
        updatedDTO.setIsbn("978-0747532699");
        updatedDTO.setPrice(new BigDecimal("39.99"));
        updatedDTO.setStockQuantity(100);
        updatedDTO.setAuthorId(1L);
        updatedDTO.setCategoryId(1L);

        when(bookService.updateBook(anyLong(), any(BookDTO.class))).thenReturn(bookDTO);

        // When & Then
        mockMvc.perform(put("/api/books/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updatedDTO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L));

        verify(bookService, times(1)).updateBook(eq(1L), any(BookDTO.class));
    }

    @Test
    void testDeleteBook() throws Exception {
        // Given
        doNothing().when(bookService).deleteBook(1L);

        // When & Then
        mockMvc.perform(delete("/api/books/1"))
                .andExpect(status().isNoContent());

        verify(bookService, times(1)).deleteBook(1L);
    }

    @Test
    void testGetBooksByAuthor() throws Exception {
        // Given
        List<BookDTO> books = Arrays.asList(bookDTO);
        when(bookService.getBooksByAuthor(1L)).thenReturn(books);

        // When & Then
        mockMvc.perform(get("/api/books/author/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].authorId").value(1L));

        verify(bookService, times(1)).getBooksByAuthor(1L);
    }

    @Test
    void testGetBooksByCategory() throws Exception {
        // Given
        List<BookDTO> books = Arrays.asList(bookDTO);
        when(bookService.getBooksByCategory(1L)).thenReturn(books);

        // When & Then
        mockMvc.perform(get("/api/books/category/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].categoryId").value(1L));

        verify(bookService, times(1)).getBooksByCategory(1L);
    }

    @Test
    void testGetAvailableBooks() throws Exception {
        // Given
        List<BookDTO> books = Arrays.asList(bookDTO);
        when(bookService.getAvailableBooks()).thenReturn(books);

        // When & Then
        mockMvc.perform(get("/api/books/available"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].stockQuantity").value(50));

        verify(bookService, times(1)).getAvailableBooks();
    }
}

