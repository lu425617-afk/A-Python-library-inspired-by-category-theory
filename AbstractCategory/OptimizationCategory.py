import numpy as np
from typing import Callable, Dict, List
from .AbstractCategory import AbstractCategory
from .Morphism import Morphism

class OptimizationCategory(AbstractCategory):
    def __init__(self, 
                 objects: List[str], 
                 morphism_association: Dict[str, Dict[str, List[Morphism]]], 
                 loss_function: Callable[[np.ndarray], float], 
                 gradient_function: Callable[[np.ndarray], np.ndarray], 
                 learning_rate: float = 0.01,
                 optimizer: str = "sgd",  # Optimizer type ('sgd', 'momentum', 'adam')
                 beta1: float = 0.9,  # For momentum and adam
                 beta2: float = 0.999,  # For adam
                 epsilon: float = 1e-8):  # For adam
        """
        Initialize an optimization category.

        :param objects: The objects in the category (e.g., names of parameters).
        :param morphism_association: The association of morphisms (mapping between objects).
        :param loss_function: The loss function.
        :param gradient_function: The gradient of the loss function.
        :param learning_rate: The learning rate.
        :param optimizer: The type of optimizer ('sgd', 'momentum', 'adam').
        :param beta1: The momentum term (used for momentum optimizer and Adam).
        :param beta2: The second moment estimate term (used for Adam).
        :param epsilon: Numerical stability term (used for Adam).
        """
        super().__init__(objects, [], morphism_association)  # Call the parent class's initializer
        self.loss_function = loss_function
        self.gradient_function = gradient_function
        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        
        # Initialize momentum and second moment estimates cache
        self.momentum_cache = {obj: np.zeros_like(np.array([0.0])) for obj in objects}
        self.moving_avg_sq_cache = {obj: np.zeros_like(np.array([0.0])) for obj in objects}

    def step(self, current_object: np.ndarray, step_num: int) -> np.ndarray:
        """
        Perform a single gradient update, simulating one step in gradient descent.

        :param current_object: The current object (parameter).
        :param step_num: The current iteration step number, used to update momentum or Adam caches.
        :return: The updated object (parameter).
        """
        # Convert the numpy array to a tuple to use as a dictionary key
        current_object_key = tuple(current_object)

        gradient = self.gradient_function(current_object)
        
        # Basic Gradient Descent (SGD)
        if self.optimizer == "sgd":
            update = self.learning_rate * gradient
        
        # Momentum (Momentum Method)
        elif self.optimizer == "momentum":
            self.momentum_cache[current_object_key] = self.beta1 * self.momentum_cache.get(current_object_key, np.zeros_like(gradient)) + (1 - self.beta1) * gradient
            update = self.learning_rate * self.momentum_cache[current_object_key]

        # Adam Optimizer
        elif self.optimizer == "adam":
            # Compute first and second moment estimates
            self.moving_avg_sq_cache[current_object_key] = self.beta2 * self.moving_avg_sq_cache.get(current_object_key, np.zeros_like(gradient)) + (1 - self.beta2) * gradient**2
            self.momentum_cache[current_object_key] = self.beta1 * self.momentum_cache.get(current_object_key, np.zeros_like(gradient)) + (1 - self.beta1) * gradient

            # Bias correction
            momentum_corrected = self.momentum_cache[current_object_key] / (1 - self.beta1**step_num)
            moving_avg_sq_corrected = self.moving_avg_sq_cache[current_object_key] / (1 - self.beta2**step_num)

            update = self.learning_rate * momentum_corrected / (np.sqrt(moving_avg_sq_corrected) + self.epsilon)
    
        # Create morphism
        morph_name = f"step_{current_object}"
        morph = Morphism(morph_name, str(current_object), str(current_object - update))
        
        # Update morphism association
        if str(current_object) not in self.morphism_association:
            self.morphism_association[str(current_object)] = {}
        self.morphism_association[str(current_object)][str(current_object - update)] = [morph]
        
        # Update the object
        return current_object - update

    def optimize(self, initial_object: np.ndarray, num_steps: int = 100) -> np.ndarray:
        """
        Perform gradient descent optimization.

        :param initial_object: The initial parameter.
        :param num_steps: The number of optimization steps.
        :return: The parameter after optimization.
        """
        current_object = initial_object
        for step in range(1, num_steps + 1):
            current_object = self.step(current_object, step)
            loss = self.loss_function(current_object)
            print(f"Step {step}/{num_steps}, Loss: {loss}")
        return current_object

    def get_loss(self, object: np.ndarray) -> float:
        """Return the current loss value for the object"""
        return self.loss_function(object)
