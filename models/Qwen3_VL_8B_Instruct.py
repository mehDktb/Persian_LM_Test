from .model_manager import _schedule_auto_unload, get_model

SQL_SCHEMA = """
CREATE TABLE [dbo].[Customers](
            [Name] [nvarchar](150) NOT NULL, 
            [CustomerType] [tinyint] NOT NULL, 
            [NationalId] [nvarchar](50) NOT NULL, 
            [PostalCode] [nvarchar](50) NOT NULL, 
            [BranchNumber] [nvarchar](50) NOT NULL, 
            [EconomicCode] [nvarchar](50) NOT NULL, 
            [IsActive] [tinyint] NOT NULL, 
            [Phone] [nvarchar](250) NOT NULL, 
            [Mobile] [nvarchar](250) NOT NULL, 
            [Address] [nvarchar](250) NOT NULL, 
            [Description] [nvarchar](250) NOT NULL, 
            [LastUpdateJalali] [nvarchar](20) NOT NULL, 
            [UpdateBy] [bigint] NOT NULL, 
            [id] [bigint] IDENTITY(1,1) NOT NULL,
        CONSTRAINT [PK_Customers] PRIMARY KEY CLUSTERED
        (
            [id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[Goods](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [TaxSystemCode] [nvarchar](50) NOT NULL, 
            [Description] [nvarchar](250) NOT NULL, 
            [GoodUnit] [bigint] NULL, 
            [TaxRate] [decimal](25, 8) NOT NULL, 
            [UserDescription] [nvarchar](250) NOT NULL, 
            [UserCode] [nvarchar](50) NOT NULL, 
            [LastUpdateJalali] [nvarchar](20) NOT NULL, 
            [UpdateBy] [bigint] NOT NULL, 
        CONSTRAINT [PK_goods] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[GoodUnits](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Name] [nvarchar](150) NOT NULL, 
        CONSTRAINT [PK_GoodUnits] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]

        
        
        CREATE TABLE [dbo].[Invoices](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [TaxId] [nvarchar](50) NOT NULL, 
            [FactorNumber] [bigint] NOT NULL, 
            [CreateDateJalali] [nvarchar](20) NULL, 
            [InvoiceType] [tinyint] NOT NULL, 
            [Pattern] [tinyint] NOT NULL, 
            [Subject] [tinyint] NOT NULL,
            [CustomerId] [bigint] NULL, 
            [PaymentMethod] [tinyint] NOT NULL, 
            [Naghdi] [bigint] NOT NULL, 
            [Nesiye] [bigint] NOT NULL, 
            [ContractCode] [nvarchar](50) NOT NULL, 
            [DeliveryStatus] [tinyint] NOT NULL, 
            [DeliveryResult] [nvarchar](4000) NULL, 
            [Description] [nvarchar](500) NULL, 
            [LastUpdateJalali] [nvarchar](20) NOT NULL, 
            [UpdateBy] [bigint] NOT NULL, 
            [TotalDiscount] [bigint] NULL, 
            [TotalPrice] [bigint] NULL, 
            [TotalTax] [bigint] NULL, 
            [NetValue] [bigint] NULL, 
            [ShowInList] [tinyint] NOT NULL, 
            [CustomCode] [nvarchar](50) NOT NULL, 
            [SendDateJalali] [nvarchar](20) NOT NULL,  
        CONSTRAINT [PK_Invoices] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

        

        CREATE TABLE [dbo].[InvoiceItems](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [GoodId] [bigint] NOT NULL, 
            [InvoceId] [bigint] NOT NULL,
            [Quantity] [decimal](25, 8) NOT NULL, 
            [TaxRate] [decimal](25, 8) NOT NULL, 
            [UnitPrice] [decimal](25, 8) NOT NULL, 
            [Discount] [bigint] NOT NULL, 
            [Description] [nvarchar](250) NULL, 
            [LastUpdateJalali] [nvarchar](20) NOT NULL, 
            [UpdateBy] [bigint] NOT NULL, 
            [TotalPrice] [bigint] NULL, 
            [TotalTax] [bigint] NULL, 
            [NetValue] [bigint] NULL, 
        CONSTRAINT [PK_InvoiceItems] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[AccountGroups](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Title] [nvarchar](150) NOT NULL, 
            [Code] [int] NOT NULL, 
            [IsActive] [tinyint] NOT NULL, 
            [Kind] [int] NOT NULL, 
            [Nature] [int] NOT NULL, 
        CONSTRAINT [PK_AccountGroups] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[AccountingDocs](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [DocNo] [bigint] NOT NULL, 
            [CreationDateJalali] [nvarchar](50) NULL, 
            [Description] [nvarchar](250) NULL, 
            [TotalDebt] [decimal](18, 0) NULL, 
            [Kind] [tinyint] NOT NULL, 
            [Status] [tinyint] NOT NULL, 
            [ApprovedBy] [bigint] NULL, 
            [ApprovalDateJalali] [nvarchar](50) NULL, 
            [TotalCredit] [decimal](18, 0) NULL, 
            [IsApproved] [tinyint] NOT NULL, 
            [DailyNo] [int] NULL, 
            [HasAttach] [bit] NOT NULL, 
        CONSTRAINT [PK_AccountingDocs] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]
        Go

        CREATE TABLE [dbo].[DocItems](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [DocId] [bigint] NULL, 
            [SubledgerId] [bigint] NULL, 
            [TotalDept] [decimal](18, 0) NOT NULL, 
            [Description] [nvarchar](250) NULL, 
            [TafsilId1] [bigint] NULL, 
            [TafsilId2] [bigint] NULL, 
            [TafsilId3] [bigint] NULL, 
            [TafsilId4] [bigint] NULL, 
            [TotalCredit] [decimal](18, 0) NOT NULL, 
        CONSTRAINT [PK_DocItems] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[Ledgers](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [Code] [int] NOT NULL, 
            [GroupId] [bigint] NOT NULL, 
            [Title] [nvarchar](150) NOT NULL, 
            [Kind] [int] NOT NULL, 
            [Nature] [int] NOT NULL, 
            [IsActive] [tinyint] NOT NULL, 
        CONSTRAINT [PK_Ledgers_1] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[SubLedgers](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Code] [int] NOT NULL, 
            [Title] [nvarchar](150) NOT NULL, 
            [LedgerId] [bigint] NOT NULL, 
            [IsActive] [tinyint] NOT NULL, 
            [Nature] [int] NOT NULL, 
            [Kind] [int] NOT NULL, 
            [TafsilId1] [bigint] NULL, 
            [TafsilId2] [bigint] NULL, 
            [TafsilId3] [bigint] NULL, 
            [TafsilId4] [bigint] NULL, 
        CONSTRAINT [PK_SubLedgers] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]

        CREATE TABLE [dbo].[Tafsils](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [Code] [int] NOT NULL, 
            [TafsilTypeId] [bigint] NOT NULL, 
            [Title] [nvarchar](150) NOT NULL, 
            [IsActive] [tinyint] NOT NULL, 
            [Description] [nvarchar](500) NULL, 
            [CustomerId] [bigint] NULL, 
        CONSTRAINT [PK_Tafsils] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[TafsilTypes](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Code] [int] NOT NULL, 
            [Title] [nvarchar](150) NOT NULL, 
            [IsSystem] [tinyint] NOT NULL, 
        CONSTRAINT [PK_TafsilTypes] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]
        
        ALTER TABLE [dbo].[DocItems]  WITH CHECK ADD  CONSTRAINT [FK_DocItems_SubLedgers] FOREIGN KEY([SubledgerId])
        REFERENCES [dbo].[SubLedgers] ([Id])

        ALTER TABLE [dbo].[DocItems]  WITH CHECK ADD  CONSTRAINT [FK_DocItems_AccountingDocs] FOREIGN KEY([DocId])
        REFERENCES [dbo].[AccountingDocs] ([Id])

        
        ALTER TABLE [dbo].[Tafsils]  WITH CHECK ADD  CONSTRAINT [FK_Tafsils_TafsilTypes] FOREIGN KEY([TafsilTypeId])
        REFERENCES [dbo].[TafsilTypes] ([Id])
        ON DELETE CASCADE
        
        ALTER TABLE [dbo].[Tafsils]  WITH CHECK ADD  CONSTRAINT [FK_Tafsils_Tafsils] FOREIGN KEY([Id])
        REFERENCES [dbo].[Tafsils] ([Id])
        
        ALTER TABLE [dbo].[Tafsils]  WITH CHECK ADD  CONSTRAINT [FK_Tafsils_Customers] FOREIGN KEY([CustomerId])
        REFERENCES [dbo].[Customers] ([Id])
        
        ALTER TABLE [dbo].[SubLedgers]  WITH CHECK ADD  CONSTRAINT [FK_SubLedgers_Ledgers] FOREIGN KEY([LedgerId])
        REFERENCES [dbo].[Ledgers] ([Id])       

        ALTER TABLE [dbo].[Ledgers]  WITH CHECK ADD  CONSTRAINT [FK_Ledgers_AccountGroups] FOREIGN KEY([GroupId])
        REFERENCES [dbo].[AccountGroups] ([Id])
        
        ALTER TABLE [dbo].[Goods]  WITH CHECK ADD  CONSTRAINT [FK_Goods_GoodUnits] FOREIGN KEY([GoodUnit])
        REFERENCES [dbo].[GoodUnits] ([Id])
        
        ALTER TABLE [dbo].[InvoiceItems]  WITH CHECK ADD  CONSTRAINT [FK_InvoiceItems_goods] FOREIGN KEY([GoodId])
        REFERENCES [dbo].[Goods] ([Id])
        
        ALTER TABLE [dbo].[InvoiceItems]  WITH CHECK ADD  CONSTRAINT [FK_InvoiceItems_Invoices] FOREIGN KEY([InvoceId])
        REFERENCES [dbo].[Invoices] ([Id])
        
        ALTER TABLE [dbo].[Invoices]  WITH NOCHECK ADD  CONSTRAINT [FK_Invoices_Customers] FOREIGN KEY([CustomerId])
        REFERENCES [dbo].[Customers] ([Id])
        NOT FOR REPLICATION 
"""


SQL_SYSTEM_PROMPT = f"""
You are an expert Microsoft SQL Server (T-SQL) database administrator.

You will receive:
- A database schema (SQL Server style, with tables, columns, and constraints).
- A user request that may be written in Persian (Farsi) or English.

Your task:
- Understand what the user wants from the database.
- Generate ONE valid, efficient T-SQL query that works with the given schema.
- Use only the tables and columns that exist in the schema.
- Prefer explicit JOINs instead of old-style joins.
- Do NOT invent new tables or columns.
- Do NOT explain the query.
- Do NOT return anything except the SQL code itself.

Database schema:
{SQL_SCHEMA}
"""


def qwen_sql_from_nl(user_text: str, schema: str = SQL_SCHEMA) -> str:
    """
    Convert a natural-language request (Persian or English) into a T-SQL query
    using Qwen3-VL-8B-Instruct, given a database schema.
    """
    model, processor = get_model("qwen")

    system_prompt = SQL_SYSTEM_PROMPT

    # Use list-of-segments format for both system and user
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": system_prompt},
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_text},
            ],
        },
    ]

    # 1) Build chat prompt string
    chat_text = processor.apply_chat_template(
        messages,
        tokenize=False,              # get plain text, not tensors
        add_generation_prompt=True,
    )

    # 2) Tokenize – IMPORTANT: use keyword argument text=..., and images=None
    inputs = processor(
        text=[chat_text],            # or text=chat_text, but list is safer (batch dim)
        images=None,
        return_tensors="pt",
    )

    # 3) Move tensors to model device
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # 4) Generate
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=False,
        top_p=1.0,
        temperature=0.0,
    )

    # 5) Strip prompt tokens
    prompt_len = inputs["input_ids"].shape[1]
    generated_ids_trimmed = generated_ids[:, prompt_len:]

    # 6) Decode
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    _schedule_auto_unload()

    sql = output_text[0].strip()

    # 7) Clean ```sql fences if present
    if sql.startswith("```"):
        sql = sql.strip("`")
        lines = sql.splitlines()
        if lines and lines[0].strip().lower() in ("sql", "tsql", "t-sql"):
            sql = "\n".join(lines[1:]).strip()

    return sql



def qwen_chat(text: str) -> str:
    """
    Run a single-turn chat with Qwen3-VL-8B-Instruct.
    Model is loaded on demand and auto-unloaded after 10 min of inactivity.
    """
    model, processor = get_model("qwen")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text,
                },
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    # Move tensors to same device as the model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
    )

    # Remove prompt tokens
    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(inputs["input_ids"], generated_ids)
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    # Refresh TTL again after generation (in case generation took long)
    _schedule_auto_unload()

    return output_text[0]
