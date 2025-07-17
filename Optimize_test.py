
import unittest
import numpy as np
from AbstractCategory.OptimizationCategory import OptimizationCategory

class TestOptimizationCategory(unittest.TestCase):

    def setUp(self):
        """设置每个测试的初始条件"""
       
        def loss_function(w: np.ndarray) -> float:
            return np.sum(w**2)  # L(w) = w^2

        def gradient_function(w: np.ndarray) -> np.ndarray:
            return 2 * w  # L'(w) = 2w

        self.loss_function = loss_function
        self.gradient_function = gradient_function

    def test_sgd_optimizer(self):
        """测试基本的梯度下降优化器"""
        initial_object = np.array([0.5])  
        optimization_category = OptimizationCategory(
            objects=["w"],
            morphism_association={},
            loss_function=self.loss_function,
            gradient_function=self.gradient_function,
            learning_rate=0.01,  
            optimizer="sgd"
        )

        optimized_object = optimization_category.optimize(initial_object, num_steps=200)  
        self.assertAlmostEqual(optimized_object[0], 0, places=1)  



    def test_adam_optimizer(self):
        """测试Adam优化器"""
        initial_object = np.array([0.5])  
        optimization_category = OptimizationCategory(
            objects=["w"],
            morphism_association={},
            loss_function=self.loss_function,
            gradient_function=self.gradient_function,
            learning_rate=0.01,  
            optimizer="adam"
        )

        optimized_object = optimization_category.optimize(initial_object, num_steps=200)  
        self.assertAlmostEqual(optimized_object[0], 0, places=1) 
if __name__ == '__main__':
    unittest.main()
