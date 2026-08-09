package com.bookstore.service;

import com.bookstore.dto.CategoryDTO;
import com.bookstore.entity.Category;
import com.bookstore.exception.ResourceNotFoundException;
import com.bookstore.repository.CategoryRepository;
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
class CategoryServiceTest {

    @Mock
    private CategoryRepository categoryRepository;

    @InjectMocks
    private CategoryService categoryService;

    private Category category;
    private CategoryDTO categoryDTO;

    @BeforeEach
    void setUp() {
        category = new Category();
        category.setId(1L);
        category.setName("Fantasy");
        category.setDescription("Fantasy fiction books");

        categoryDTO = new CategoryDTO();
        categoryDTO.setId(1L);
        categoryDTO.setName("Fantasy");
        categoryDTO.setDescription("Fantasy fiction books");
    }

    @Test
    void testGetAllCategories() {
        // Given
        List<Category> categories = Arrays.asList(category);
        when(categoryRepository.findAll()).thenReturn(categories);

        // When
        List<CategoryDTO> result = categoryService.getAllCategories();

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("Fantasy", result.get(0).getName());
        verify(categoryRepository, times(1)).findAll();
    }

    @Test
    void testGetCategoryById_Success() {
        // Given
        when(categoryRepository.findById(1L)).thenReturn(Optional.of(category));

        // When
        CategoryDTO result = categoryService.getCategoryById(1L);

        // Then
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("Fantasy", result.getName());
        verify(categoryRepository, times(1)).findById(1L);
    }

    @Test
    void testGetCategoryById_NotFound() {
        // Given
        when(categoryRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> categoryService.getCategoryById(1L));
        verify(categoryRepository, times(1)).findById(1L);
    }

    @Test
    void testCreateCategory_Success() {
        // Given
        CategoryDTO newCategoryDTO = new CategoryDTO();
        newCategoryDTO.setName("Science Fiction");
        newCategoryDTO.setDescription("Sci-fi books");

        Category savedCategory = new Category();
        savedCategory.setId(2L);
        savedCategory.setName("Science Fiction");
        savedCategory.setDescription("Sci-fi books");

        when(categoryRepository.save(any(Category.class))).thenReturn(savedCategory);

        // When
        CategoryDTO result = categoryService.createCategory(newCategoryDTO);

        // Then
        assertNotNull(result);
        assertEquals("Science Fiction", result.getName());
        verify(categoryRepository, times(1)).save(any(Category.class));
    }

    @Test
    void testUpdateCategory_Success() {
        // Given
        CategoryDTO updatedDTO = new CategoryDTO();
        updatedDTO.setName("Updated Category");
        updatedDTO.setDescription("Updated Description");

        when(categoryRepository.findById(1L)).thenReturn(Optional.of(category));
        when(categoryRepository.save(any(Category.class))).thenReturn(category);

        // When
        CategoryDTO result = categoryService.updateCategory(1L, updatedDTO);

        // Then
        assertNotNull(result);
        verify(categoryRepository, times(1)).findById(1L);
        verify(categoryRepository, times(1)).save(any(Category.class));
    }

    @Test
    void testUpdateCategory_NotFound() {
        // Given
        when(categoryRepository.findById(1L)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> categoryService.updateCategory(1L, categoryDTO));
        verify(categoryRepository, times(1)).findById(1L);
        verify(categoryRepository, never()).save(any(Category.class));
    }

    @Test
    void testDeleteCategory_Success() {
        // Given
        when(categoryRepository.existsById(1L)).thenReturn(true);
        doNothing().when(categoryRepository).deleteById(1L);

        // When
        categoryService.deleteCategory(1L);

        // Then
        verify(categoryRepository, times(1)).existsById(1L);
        verify(categoryRepository, times(1)).deleteById(1L);
    }

    @Test
    void testDeleteCategory_NotFound() {
        // Given
        when(categoryRepository.existsById(1L)).thenReturn(false);

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> categoryService.deleteCategory(1L));
        verify(categoryRepository, times(1)).existsById(1L);
        verify(categoryRepository, never()).deleteById(anyLong());
    }
}

