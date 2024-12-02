# Foodpangolin

## Class diagram
```mermaid
classDiagram
    class 商家 {
        +int id
        +string name
        +string location
        +string contactInfo
        +list<菜單> menu
        +void uploadMenu()
        +void confirmOrder(Order order)
        +void notifyPickup(Order order)
        +list<Order> viewOrderHistory()
    }

    class 送貨員 {
        +int id
        +string name
        +string vehicleInfo
        +string contactInfo
        +list<訂單> assignedOrders
        +void acceptOrder(Order order)
        +void updateDeliveryStatus(Order order, string status)
        +list<訂單> viewDeliveryHistory()
    }

    class 顧客 {
        +int id
        +string name
        +string contactInfo
        +string address
        +list<訂單> orderHistory
        +void browseMenu(商家 merchant)
        +void placeOrder(Order order)
        +void trackOrder(Order order)
        +void leaveFeedback(Order order, string feedback)
    }

    class 菜單 {
        +int id
        +string name
        +float price
        +string description
        +string availabilityStatus
    }

    class 訂單 {
        +int id
        +顧客 customer
        +商家 merchant
        +送貨員 deliveryPerson
        +list<菜單> items
        +string status
        +string deliveryAddress
        +float totalPrice
        +void updateStatus(string newStatus)
    }

    商家 --|> 菜單 : 管理
    商家 <|-- 訂單 : 收
    顧客 --|> 訂單 : 發
    送貨員 <|-- 訂單 : 送
    訂單 <--> MenuItem : 相關

```

## Sequence diagram
```mermaid
sequenceDiagram
    participant Customer as 顧客
    participant Merchant as 商家
    participant DeliveryPerson as 送貨員

    Customer->>Merchant: 瀏覽菜單
    Merchant-->>Customer: 返回菜單列表
    Customer->>Merchant: 下訂單
    Merchant-->>Customer: 確認訂單

    Merchant->>DeliveryPerson: 指派送貨訂單
    DeliveryPerson-->>Merchant: 接受送貨訂單

    DeliveryPerson->>Merchant: 到店取餐
    Merchant-->>DeliveryPerson: 餐點交接完成

    DeliveryPerson->>Customer: 送達訂單
    Customer-->>DeliveryPerson: 確認收餐並給評價

    Customer->>Merchant: 給予商家評價
    Merchant-->>Customer: 感謝評價
```

## Data flow
```mermaid
flowchart TD
    subgraph ExternalEntities
        C[顧客]
        M[商家]
        D[送貨員]
    end

    subgraph System[點餐平台系統]
        DB[(資料庫)]
        MGT[菜單管理]
        OPM[訂單處理模組]
        DEL[送貨分配模組]
        FEEDBACK[評價管理模組]
    end

    %% 顧客流程
    C -->|瀏覽菜單| MGT
    MGT -->|提供菜單資訊| C
    C -->|下訂單| OPM
    OPM -->|保存訂單| DB
    OPM -->|通知商家| M

    %% 商家流程
    M -->|更新菜單| MGT
    MGT -->|保存菜單數據| DB
    M -->|確認訂單| OPM
    OPM -->|分配送貨員| DEL
    DEL -->|通知送貨員| D

    %% 送貨員流程
    D -->|接收送貨任務| DEL
    DEL -->|更新送貨狀態| DB
    D -->|完成配送| OPM

    %% 評價流程
    C -->|提交評價| FEEDBACK
    FEEDBACK -->|保存評價| DB
    FEEDBACK -->|提供評價數據| M
    FEEDBACK -->|提供評價數據| D
```

## Entity Relationship Diagram
```mermaid
erDiagram
    Customer {
        int id PK
        string name
        string contact_info
        string address
    }
    
    Merchant {
        int id PK
        string name
        string location
        string contact_info
    }

    DeliveryPerson {
        int id PK
        string name
        string vehicle_info
        string contact_info
    }
    
    MenuItem {
        int id PK
        string name
        float price
        string description
        string availability_status
        int merchant_id FK
    }

    Order {
        int id PK
        int customer_id FK
        int merchant_id FK
        int delivery_person_id FK
        string status
        string delivery_address
        float total_price
        datetime created_at
    }

    OrderItem {
        int id PK
        int order_id FK
        int menu_item_id FK
        int quantity
        float price
    }

    Feedback {
        int id PK
        int customer_id FK
        int target_id FK
        string feedback_text
        int rating
        datetime created_at
    }

    %% Relationships
    Customer ||--o{ Order : "發"
    Merchant ||--o{ MenuItem : "提供"
    Merchant ||--o{ Order : "接收"
    DeliveryPerson ||--o{ Order : "運送"
    Order ||--o{ OrderItem : "包含"
    MenuItem ||--o{ OrderItem : "被放進"
    Customer ||--o{ Feedback : "評價"
    Feedback }o--|| Merchant : "給商家"
    Feedback }o--|| DeliveryPerson : "給送貨員"
```

## MVC
```
project/
├── app/
│   ├── __init__.py       # 初始化 Flask
│   ├── controllers/
│   │   ├── customer_controller.py
│   │   ├── merchant_controller.py
│   │   ├── delivery_person_controller.py
│   │   ├── order_controller.py
│   │   ├── feedback_controller.py
│   │   └── menu_item_controller.py
│   │
│   ├── models/
│   │   ├── __init__.py   # 初始化 SQL 模組
│   │   ├── customer.py
│   │   ├── merchant.py
│   │   ├── delivery_person.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── feedback.py
│   │   └── menu_item.py
│   │
│   ├── templates/
│   │   ├── customer/
│   │   │   ├── browse_menu.html
│   │   │   ├── place_order.html
│   │   │   └── order_history.html
│   │   ├── merchant/
│   │   │   ├── dashboard.html
│   │   │   ├── manage_menu.html
│   │   │   └── order_list.html
│   │   ├── delivery_person/
│   │   │   ├── assigned_orders.html
│   │   │   ├── update_status.html
│   │   │   └── delivery_history.html
│   │   └── shared/
│   │       ├── layout.html
│   │       └── navbar.html
│   │
│   └── static/
│       ├── css/
│       │   ├── style.css
│       │   └── merchant.css
│       ├── js/
│       │   ├── scripts.js
│       │   └── customer.js
│       └── images/
│           ├── logo.png
│           └── banner.jpg
│
├── config/
│   ├── __init__.py
│   ├── settings.py       # 設定檔案 (如資料庫帳密設定)
│   ├── routes.py         # 路由設計
│   └── database.py       # 初始化資料庫連線
│
├── tests/
│   ├── test_customer_controller.py
│   ├── test_order_controller.py
│   ├── test_feedback_flow.py
│   └── test_order_flow.py
│
├── .env                  # 環境變數
├── .gitignore
├── README.md
├── requirements.txt      # 版本控制
└── run.py                # 入口
```

### MVC 流程示例
顧客下訂單的流程

1. View:
    - 顧客通過 `templates/customer/browse_menu.html` 瀏覽菜單。
2. Controller:
    - `customer_controller.py` 中的 `place_order()` 方法處理訂單資料。
3. Model:
    - `models/order.py` 將訂單保存至資料庫。
4. Response:
    - 訂單生成後，返回確認頁面 `templates/customer/place_order.html`。
