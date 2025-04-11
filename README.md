# Payment Analytics & Consolidated Payment System

## Overview
A data analytics project using PostgreSQL to analyze loan repayment patterns and develop a consolidated payment solution for customers with multiple financial contracts. This project includes both data generation scripts and SQL queries for analyzing payment behavior.

## Project Purpose
This project demonstrates how to:
- Track and analyze payment patterns across different loan types
- Identify factors influencing on-time vs. late payments
- Design and simulate a consolidated payment system
- Allocate payments efficiently across multiple contracts
- Create meaningful customer segments based on payment reliability

## Repository Structure
- `bank_analytics/` - Main project directory
  - `generate_data.py` - Data generation script
  - `data_generators/` - Data generation modules
  - `db/` - Database connection utilities
  - `schema/` - SQL schema definitions
  - `utils/` - Helper functions
  - `sql/` - Analysis queries

## Data Model
The database includes:
- Customers table with risk profiles
- Products with different types and interest rates
- Contracts linking customers to specific products
- Payments with detailed status tracking
- Customer service interactions

## Key Features
- Payment pattern analysis
- Customer segmentation by payment behavior
- Consolidated payment allocation logic
- Advanced SQL analytics with window functions
- Time-series payment trend analysis

## Getting Started
1. Set up PostgreSQL database
2. Configure environment variables in .env file
3. Run data generation script
4. Execute analysis queries
