

 # Payment Analytics Project

## Overview
A PostgreSQL-based data analysis project focused on loan repayment behavior and consolidated payment solutions. 

## Project Purpose
The project allows financial analysts to:
- Identify patterns in customer payment behavior
- Analyze late payment statistics across product types
- Design consolidated payment solutions for multi-contract customers
- Create performance dashboards for loan portfolios
- Generate customer segmentation based on payment reliability

## Repository Structure
- `bank_analytics/` - Main project directory
  - `generate_data.py` - Data generation script
  - `data_generators/` - Data generation modules for each entity
  - `db/` - Database connection utilities
  - `schema/` - SQL schema definitions
  - `utils/` - Helper functions
  - `analysis/` - SQL analysis queries

## Data Model
The project includes tables for:
- Customers with risk profiles and acquisition metrics
- Financial products (loans, BNPL, hire purchase)
- Contracts linking customers to products
- Payment transactions with detailed status tracking
- Customer service interactions

## SQL Highlights
The repository demonstrates advanced SQL techniques including:
- Time-based cohort analysis
- Customer segmentation using CASE statements
- Financial metric calculations
- Product performance comparisons
- Window functions for payment pattern analysis

## Getting Started
1. Set up PostgreSQL and create database
2. Create .env file with database credentials
3. Run `generate_data.py` to create sample data
4. Execute SQL queries to analyze payment patterns
