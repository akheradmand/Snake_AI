<h1>Snake Game with AI</h1>

# Description

In this project, first, the snake automatically moves towards the apple with rules (if, else, ...) and the information needed to produce the dataset is collected and stored.
This information includes the distance of the snake from the walls, the coordinates of the snake, the coordinates of the apple and the presence or absence of the apple around the snake.

![Alt text](assets/direction.png)

# How to install

'pip install -r requirements.txt'

# How to run

1- Generate dataset:
'python generate_dataset.py'

2- Train neural network:
'python train.py'

3- See the result
'python main_ml.py'

# Results

![Alt text](assets/loss_accuracy.png)

![Alt text](assets/loss_accuracy_fig.png)

![Alt text](assets/snake_ai.png)