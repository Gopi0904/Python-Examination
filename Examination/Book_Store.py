import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import datetime

sns.set_theme(style="whitegrid")

class BookStore:
    def __init__(self, inventory_file, sales_file):
        self.inventory_file = inventory_file
        self.sales_file = sales_file
        self.inventory = pd.read_csv(inventory_file)
        self.sales = pd.read_csv(sales_file)

    def add_book(self, title, author, genre, price, quantity):
        new_book = {
            'Title': title,
            'Author': author,
            'Genre': genre,
            'Price': float(price),
            'Quantity': int(quantity)
        }
        self.inventory = pd.concat([self.inventory, pd.DataFrame([new_book])], ignore_index=True)
        self.save_inventory()
        print("✅ Book added successfully!")
    
    def update_inventory(self, title, quantity):
        if title not in self.inventory['Title'].values:
            print("❌ Book not found in inventory.")
            return
        self.inventory.loc[self.inventory['Title'] == title, 'Quantity'] = int(quantity)
        self.save_inventory()
        print("✅ Inventory Updated successdully!")

    def generate_report(self):
        print("\n=== Inventory Summary ===")
        print(self.inventory)
        print("\n=== Sales Summary ===")
        print(self.sales.tail()) 

    def save_inventory(self):
        self.inventory.to_csv(self.inventory_file, index=False)

    def save_sales(self):
        self.sales.to_csv(self.sales_file, index=False)

    def sales_analysis(self):
        print("\n=== Sales Analysis ===")
        df = self.sales.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        total_revenue = df['Total Revenue'].sum()
        avg_price = np.mean(df['Total Revenue'] / df['Quantity Sold'])
        top_books = df.groupby('Title')['Quantity Sold'].sum().sort_values(ascending=False)
        print(f"Total Revenue: {total_revenue}")
        print(f"Average Selling Price: {avg_price:.2f}")
        print("Top Selling Books:\n", top_books.head())

    def visualize_data(self):
        print("\n==== Book Store Visualizations ====")
        print("1. Bar Chart – Total Sales by Genre")
        print("3. Pie Chart – Revenue Share by Genre")
        print("4. Heatmap – Price vs Sales Volume")
        print("5. Line Chart – Monthly Revenue Trend")

        choice = int(input("Enter your choice (1-5): "))

        data = self.sales.copy()
        data["Date"] = pd.to_datetime(data["Date"])

        if choice == 1:
            merged = pd.merge(data, self.inventory[["Title", "Genre"]])
            genre_totals = merged.groupby("Genre")["Total Revenue"].sum()
            genre_totals.plot(kind="bar", color="skyblue", figsize=(8, 4))
            plt.title("Total Revenue by Genre")
            plt.ylabel("Revenue")
            plt.show()

        elif choice == 3:
            merged = pd.merge(data, self.inventory[["Title", "Genre"]])
            genre_share = merged.groupby("Genre")["Total Revenue"].sum()
            genre_share.plot(kind="pie", startangle=90,figsize=(6, 6))
            plt.title("Revenue Share by Genre")
            plt.ylabel("")
            plt.show()

        elif choice == 4:
            merged = pd.merge(data, self.inventory[["Title", "Price"]])
            stats = merged.groupby("Title").agg({"Price": "mean","Quantity Sold": "sum"}).rename(columns={"Quantity Sold": "Total Sold"})
            sns.heatmap(stats.corr(), annot=True, cmap="coolwarm", square=True)
            plt.title("Correlation: Price vs Sales Volume")
            plt.show()

        elif choice == 5:
            data["YearMonth"] = data["Date"].dt.to_period("M").astype(str)
            monthly = data.groupby("YearMonth")["Total Revenue"].sum()
            monthly.plot(kind="line", marker="o", color="orange", figsize=(8, 4))
            plt.title("Monthly Revenue Trend")
            plt.xlabel("Year-Month")
            plt.ylabel("Revenue")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        else:
            print("Please enter a number between 1 and 5 only.")

while True:
    print("\n===== Book Store Management =====\n")
    print("1. Load Data")
    print("2. Add Book")
    print("3. Update Inventory")
    print("4. Generate Report")
    print("5. Sales Analysis")
    print("6. Visualize Data")
    print("7. Exit\n")

    choice = int(input("\nEnter your choice (1-8) : "))

    if choice == 1:
        inventory_file = input("Enter inventory file's path : ")
        sales_file = input("Enter sales file's path : ")
        store = BookStore(inventory_file=inventory_file, sales_file=sales_file)
        print("Data Loaded Successfully! 👍")

    elif choice == 2:
        title = input("Enter book's title : ")
        author = input("Enter book's author :")
        genre = input("Enter book's genre : ")
        price = int(input("Enter book's price :"))
        quantity = int(input("Enter book's quantity : "))
        store.add_book(title=title, author=author, genre=genre, price=price, quantity=quantity)

    elif choice == 3:
        title = input("Enter book's title : ")
        quantity = int(input("Enter new quantity : "))
        store.update_inventory(title=title, quantity=quantity)

    elif choice == 4:
        store.generate_report()

    elif choice == 5:
        store.sales_analysis()

    elif choice == 6:
        store.visualize_data()
    
    elif choice == 7:
        print("You Have Exited the program successfully! 😊👋")
        break

    else:
        print("Please enter a number between 1 and 8 only.")