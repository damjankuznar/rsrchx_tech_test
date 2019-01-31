Rsrchx Tech Test
================

## Setting up the REST API backend
This guide assumes you have Docker and Docker Compose installed.

**Build the Docker images**  
```bash
docker-compose build
```

**Run the backend**  
```bash
docker-compose up -d
```

**Load food data**  
This will load example food records.
```bash
docker-compose run backend python manage.py loaddata backend/fixtures/foods.json
``` 

**Create a new user**  
The following command will prompt you for username and password. 
```bash
docker-compose run backend python manage.py createuser
```

**Create a new admin user**  
The following command will prompt you for username, email and password. 
```bash
docker-compose run backend python manage.py createsuperuser
```

## Using the command line client
You will enter the backend container with the following command from which you will
have access to the client command line script and will be able to query REST API backend
with it.
```bash
 docker-compose exec backend bash
```

### Public methods
**List foods**
```bash
./client.py foods list
```
**Food details**
```bash
./client.py foods detail {food_id}
```

### Private methods
To access private methods you need to login as a user first with the following command, 
where `{user}` is a username that you used for registering. 
```bash
./client.py login {user}
```

**View cart**
```bash
./client.py cart view
```

**Add item to cart**
```bash
./client.py cart add {food_id} {quantity}
```

**Add item to cart**
```bash
./client.py cart remove {item_id}
```

**Submit the order**
```bash
./client.py cart checkout
```

**List orders**
```bash
./client.py orders list
```

**View order details**
```bash
./client.py orders details {order_id}
```

### Admin method
To access admin methods you need to login as an admin first.

**List pending orders**
```bash
./client.py admin orders list
```

**View order details**
```bash
./client.py admin orders details {order_id}
```

**Mark order as completed**
```bash
./client.py admin orders completed {order_id}
```

## Running tests
The following command will execute tests in container and output the test code coverage information.
```bash
docker-compose run backend pytest --cov
```


## Tech Test Requirements
Build a command line app for a food delivery service. The customer user interface should
present the user with the ability to:

1. List foods
2. Pick a food and read more about it
3. Add one or more food items to a cart
4. View cart
5. Checkout (assume payment goes through)
6. View order details

**The food delivery service user will be able to:**
1. See pending orders
2. Mark order as delivered to clear it off the list

When the food delivery service user marks an order as delivered, the customer user should see
that reflected on his order details.
The command line app should talk to a backend via a REST API. You can use any frameworks
of your choice, but please stick to python for language choice.

**What would we assess:**
1. Data model design
2. Bug free execution
3. Test coverage
4. REST API design
5. Separation of concerns
6. Easy to follow instructions to test and execute

**What we don’t expect to see:**
1. A full fledged Auth framework
2. Session Management
3. Any other production-grade software concerns like performance, monitoring, security,
containerisation etc.