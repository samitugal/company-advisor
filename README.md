# Company Advisor

## About the Project

Company Advisor is a software solution designed to help companies optimize their business processes. This project automates tasks such as data analysis, file management, and web research using various tools and plugins.

## Main Components

### 1. Agents

The project utilizes different agents to perform specific tasks:

- **PythonAgent**: Capable of writing and executing Python code. It assists managers by generating graphs and performing calculations.
- **ResearcherAgent**: Conducts web research to find trending products and analyze competitors' financial statuses.
- **WarehouseAgent**: Provides information related to warehouse management by executing database queries.
- **FileAgent**: Handles file reading and writing operations.

### 2. Plugins

- **WarehousePlugin**: A plugin used for database queries. It interacts with a PostgreSQL database.
- **FilePlugin**: A plugin used for file reading and writing operations.

### 3. Database

The project uses a PostgreSQL database to perform data storage and querying operations. Database connections and query executions are managed by the `PostgresDB` class.

#### Optional: Northwind Database

For demonstration purposes, you can optionally set up the Northwind database. This is a sample database that can be used to test the functionality of the project.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file and add the necessary API keys and database connection details.

3. **Optional**: Initialize the Northwind database:
   ```bash
   psql -U northwind_user -d northwind -f data/northwind.sql
   ```

   Ensure you have a PostgreSQL database server running and accessible. You can connect to any existing PostgreSQL database by updating the connection details in the `PostgresDB` class.

## Usage

To run the agents and perform specific tasks, execute the `src/main.py` file. For example, to retrieve the top 5 customers by sales and generate a pie chart, use the following command:

## Screenshots
<img width="1431" alt="Screenshot at Feb 22 15-01-27" src="https://github.com/user-attachments/assets/a070e6cf-b4c9-4ff0-84e7-c19e9259e776" />

<img width="1076" alt="Screenshot at Feb 22 15-01-55" src="https://github.com/user-attachments/assets/530ed01b-fe9f-4b72-821d-73503bb72ea0" />

## Contributing

If you would like to contribute, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License. For more details, see the `LICENSE` file.

## Contact

If you have any questions or feedback, please contact us at [tugalsami@gmail.com]
