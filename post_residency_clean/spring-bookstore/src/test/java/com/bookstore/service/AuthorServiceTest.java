package com.bookstore.service;

import com.bookstore.dto.AuthorDTO;
import com.bookstore.entity.Author;
import com.bookstore.exception.ResourceNotFoundException;
import com.bookstore.repository.AuthorRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthorServiceTest {

    @Mock
    private AuthorRepository authorRepository;

    @InjectMocks
    private AuthorService authorService;

    private Author author;
    private AuthorDTO authorDTO;

    @BeforeEach
    void setUp() {
        author = new Author();
        author.setId(1L);
        author.setName("J.K. Rowling");
        author.setBiography("British author, best known for the Harry Potter series");

        authorDTO = new AuthorDTO();
        authorDTO.setId(1L);
        authorDTO.setName("J.K. Rowling");
        authorDTO.setBiography("British author, best known for the Harry Potter series");
    }

    @Test
    void testGetAllAuthors() {
        // Given
        List<Author> authors = Arrays.asList(author);
        when(authorRepository.findAll()).thenReturn(authors);

        // When
        List<AuthorDTO> result = authorService.getAllAuthors();

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("J.K. Rowling", result.get(0).getName());
        verify(authorRepository, times(1)).findAll();
    }

    @Test
    void testGetAuthorById_Success() {
        // Given
        when(authorRepository.findById(1L)).thenReturn(Optional.of(author));

        // When
        AuthorDTO result = authorService.getAuthorById(1L);

        // Then
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("J.K. Rowling", result.getName());
        verify(authorRepository, times(1)).findById(1L);
    }

    @Test
    void testGetAuthorById_NotFound() {
        // Given
        when(authorRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> authorService.getAuthorById(1L));
        verify(authorRepository, times(1)).findById(1L);
    }

    @Test
    void testCreateAuthor_Success() {
        // Given
        AuthorDTO newAuthorDTO = new AuthorDTO();
        newAuthorDTO.setName("George R.R. Martin");
        newAuthorDTO.setBiography("American novelist");

        Author savedAuthor = new Author();
        savedAuthor.setId(2L);
        savedAuthor.setName("George R.R. Martin");
        savedAuthor.setBiography("American novelist");

        when(authorRepository.save(any(Author.class))).thenReturn(savedAuthor);

        // When
        AuthorDTO result = authorService.createAuthor(newAuthorDTO);

        // Then
        assertNotNull(result);
        assertEquals("George R.R. Martin", result.getName());
        verify(authorRepository, times(1)).save(any(Author.class));
    }

    @Test
    void testUpdateAuthor_Success() {
        // Given
        AuthorDTO updatedDTO = new AuthorDTO();
        updatedDTO.setName("Updated Name");
        updatedDTO.setBiography("Updated Biography");

        when(authorRepository.findById(1L)).thenReturn(Optional.of(author));
        when(authorRepository.save(any(Author.class))).thenReturn(author);

        // When
        AuthorDTO result = authorService.updateAuthor(1L, updatedDTO);

        // Then
        assertNotNull(result);
        verify(authorRepository, times(1)).findById(1L);
        verify(authorRepository, times(1)).save(any(Author.class));
    }

    @Test
    void testUpdateAuthor_NotFound() {
        // Given
        when(authorRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> authorService.updateAuthor(1L, authorDTO));
        verify(authorRepository, times(1)).findById(1L);
        verify(authorRepository, never()).save(any(Author.class));
    }

    @Test
    void testDeleteAuthor_Success() {
        // Given
        when(authorRepository.existsById(1L)).thenReturn(true);
        doNothing().when(authorRepository).deleteById(1L);

        // When
        authorService.deleteAuthor(1L);

        // Then
        verify(authorRepository, times(1)).existsById(1L);
        verify(authorRepository, times(1)).deleteById(1L);
    }

    @Test
    void testDeleteAuthor_NotFound() {
        // Given
        when(authorRepository.existsById(1L)).thenReturn(false);

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> authorService.deleteAuthor(1L));
        verify(authorRepository, times(1)).existsById(1L);
        verify(authorRepository, never()).deleteById(anyLong());
    }
}

