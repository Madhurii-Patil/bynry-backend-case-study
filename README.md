# StockFlow Case Study - Madhuri Patil

## Part 1: Code Review & Debugging
**Identified Issues:**
1. **Atomicity Violation:** The original code committed to the database twice. If the second commit failed, it caused data corruption. I fixed this by using a single atomic commit.
2. **Data Model Error:** The `warehouse_id` was incorrectly placed in the `Product` table. I moved it to the `Inventory` logic.
3. **No Validation:** Added checks for negative prices and missing fields.

## Part 2: Database Design
I designed the schema to separate the **Product Definition** from **Inventory Storage**.
- **Key Decision:** Created a dedicated `inventory` table. This allows one product (like an iPhone) to exist in multiple warehouses (Main & Backup) with different quantities.
- **Bundles:** Used a self-referencing table to handle product bundles.

## Part 3: API Implementation
- Implemented `GET /api/companies/{id}/alerts/low-stock`.
- **Logic:** I assumed a helper function `get_sales_velocity` exists to calculate how fast items are selling, which is required to calculate `days_until_stockout`.