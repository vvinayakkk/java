package com.bookstore.controller;

import com.bookstore.dto.CategoryDTO;
import com.bookstore.service.CategoryService;
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
class CategoryControllerTest {

    private MockMvc mockMvc;

    @Mock
    private CategoryService categoryService;

    @InjectMocks
    private CategoryController categoryController;

    private ObjectMapper objectMapper;

    private CategoryDTO categoryDTO;

    @BeforeEach
    void setUp() {
        objectMapper = new ObjectMapper();
        objectMapper.findAndRegisterModules();
        mockMvc = MockMvcBuilders.standaloneSetup(categoryController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setMessageConverters(new MappingJackson2HttpMessageConverter(objectMapper))
                .build();
        
        categoryDTO = new CategoryDTO();
        categoryDTO.setId(1L);
        categoryDTO.setName("Fantasy");
        categoryDTO.setDescription("Fantasy fiction books");
    }

    @Test
    void testGetAllCategories() throws Exception {
        // Given
        List<CategoryDTO> categories = Arrays.asList(categoryDTO);
        when(categoryService.getAllCategories()).thenReturn(categories);

        // When & Then
        mockMvc.perform(get("/api/categories"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].name").value("Fantasy"));

        verify(categoryService, times(1)).getAllCategories();
    }

    @Test
    void testGetCategoryById() throws Exception {
        // Given
        when(categoryService.getCategoryById(1L)).thenReturn(categoryDTO);

        // When & Then
        mockMvc.perform(get("/api/categories/1"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.name").value("Fantasy"));

        verify(categoryService, times(1)).getCategoryById(1L);
    }

    @Test
    void testCreateCategory() throws Exception {
        // Given
        CategoryDTO newCategoryDTO = new CategoryDTO();
        newCategoryDTO.setName("Science Fiction");
        newCategoryDTO.setDescription("Sci-fi books");

        when(categoryService.createCategory(any(CategoryDTO.class))).thenReturn(categoryDTO);

        // When & Then
        mockMvc.perform(post("/api/categories")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(newCategoryDTO)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1L));

        verify(categoryService, times(1)).createCategory(any(CategoryDTO.class));
    }

    @Test
    void testCreateCategory_InvalidInput() throws Exception {
        // Given - Missing required name field
        CategoryDTO invalidCategoryDTO = new CategoryDTO();
        invalidCategoryDTO.setName(""); // Empty name should fail validation

        // When & Then
        mockMvc.perform(post("/api/categories")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidCategoryDTO)))
                .andExpect(status().isBadRequest());

        verify(categoryService, never()).createCategory(any(CategoryDTO.class));
    }

    @Test
    void testUpdateCategory() throws Exception {
        // Given
        CategoryDTO updatedDTO = new CategoryDTO();
        updatedDTO.setName("Updated Category");
        updatedDTO.setDescription("Updated Description");

        when(categoryService.updateCategory(anyLong(), any(CategoryDTO.class))).thenReturn(categoryDTO);

        // When & Then
        mockMvc.perform(put("/api/categories/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updatedDTO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L));

        verify(categoryService, times(1)).updateCategory(eq(1L), any(CategoryDTO.class));
    }

    @Test
    void testDeleteCategory() throws Exception {
        // Given
        doNothing().when(categoryService).deleteCategory(1L);

        // When & Then
        mockMvc.perform(delete("/api/categories/1"))
                .andExpect(status().isNoContent());

        verify(categoryService, times(1)).deleteCategory(1L);
    }
}

