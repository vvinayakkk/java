package com.bookstore.controller;

import com.bookstore.dto.AuthorDTO;
import com.bookstore.service.AuthorService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.bookstore.exception.GlobalExceptionHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class AuthorControllerTest {

    private MockMvc mockMvc;

    @Mock
    private AuthorService authorService;

    @InjectMocks
    private AuthorController authorController;

    private ObjectMapper objectMapper;

    private AuthorDTO authorDTO;

    @BeforeEach
    void setUp() {
        objectMapper = new ObjectMapper();
        objectMapper.findAndRegisterModules();
        mockMvc = MockMvcBuilders.standaloneSetup(authorController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setMessageConverters(new MappingJackson2HttpMessageConverter(objectMapper))
                .build();
        
        authorDTO = new AuthorDTO();
        authorDTO.setId(1L);
        authorDTO.setName("J.K. Rowling");
        authorDTO.setBiography("British author, best known for the Harry Potter series");
    }

    @Test
    void testGetAllAuthors() throws Exception {
        // Given
        List<AuthorDTO> authors = Arrays.asList(authorDTO);
        when(authorService.getAllAuthors()).thenReturn(authors);

        // When & Then
        mockMvc.perform(get("/api/authors"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].name").value("J.K. Rowling"));

        verify(authorService, times(1)).getAllAuthors();
    }

    @Test
    void testGetAuthorById() throws Exception {
        // Given
        when(authorService.getAuthorById(1L)).thenReturn(authorDTO);

        // When & Then
        mockMvc.perform(get("/api/authors/1"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("J.K. Rowling"));

        verify(authorService, times(1)).getAuthorById(1L);
    }

    @Test
    void testCreateAuthor() throws Exception {
        // Given
        AuthorDTO newAuthorDTO = new AuthorDTO();
        newAuthorDTO.setName("George R.R. Martin");
        newAuthorDTO.setBiography("American novelist");

        when(authorService.createAuthor(any(AuthorDTO.class))).thenReturn(authorDTO);

        // When & Then
        mockMvc.perform(post("/api/authors")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(newAuthorDTO)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1L));

        verify(authorService, times(1)).createAuthor(any(AuthorDTO.class));
    }

    @Test
    void testCreateAuthor_InvalidInput() throws Exception {
        // Given - Missing required name field
        AuthorDTO invalidAuthorDTO = new AuthorDTO();
        invalidAuthorDTO.setName(""); // Empty name should fail validation

        // When & Then
        mockMvc.perform(post("/api/authors")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidAuthorDTO)))
                .andExpect(status().isBadRequest());

        verify(authorService, never()).createAuthor(any(AuthorDTO.class));
    }

    @Test
    void testUpdateAuthor() throws Exception {
        // Given
        AuthorDTO updatedDTO = new AuthorDTO();
        updatedDTO.setName("Updated Name");
        updatedDTO.setBiography("Updated Biography");

        when(authorService.updateAuthor(anyLong(), any(AuthorDTO.class))).thenReturn(authorDTO);

        // When & Then
        mockMvc.perform(put("/api/authors/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updatedDTO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L));

        verify(authorService, times(1)).updateAuthor(eq(1L), any(AuthorDTO.class));
    }

    @Test
    void testDeleteAuthor() throws Exception {
        // Given
        doNothing().when(authorService).deleteAuthor(1L);

        // When & Then
        mockMvc.perform(delete("/api/authors/1"))
                .andExpect(status().isNoContent());

        verify(authorService, times(1)).deleteAuthor(1L);
    }
}

