# Payment Analytics & Consolidated Payment System

## Overview
A PostgreSQL data analytics project for analyzing banking customer behavior and product performance. Features SQL queries for payment pattern analysis and a consolidated payment solution for customers with multiple contracts. Includes both data generation scripts and analytical queries with business insights.

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
