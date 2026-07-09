For designing an inventory database, consider the following key entities and their relationships:

1. **Product** - Each product has attributes such as Product ID, Name, Category, Price, Quantity On Hand (QOH), etc.
2. **Inventory Transactions** - A transaction can be a Sale, Purchase, or Return/Issue. Attributes might include Transaction ID, Date, Type (Sale/Purchase/Return), Quantity, Unit Price, and associated product ID.

Primary Keys:
- Product: Product ID
- Inventory Transactions: Transaction ID

Foreign Keys:
- Product's QOH is linked to the primary key of another row in itself through foreign keys.
- Each transaction references a product with its Product ID.

Indexes could be used on frequently searched columns such as Product Name, Category for faster searches. 

This design allows tracking products and their transactions effectively, including managing stock levels and monitoring inventory changes over time.