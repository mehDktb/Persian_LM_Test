from .model_manager import _schedule_auto_unload, get_model

delimiter_1="****"

SQL_SCHEMA = f"""
CREATE TABLE [dbo].[Customers](
            [Name] [nvarchar](150) NOT NULL, --{delimiter_1} نام_خریدار
            [CustomerType] [tinyint] NOT NULL, --{delimiter_1} نوع_خریدار
            [NationalId] [nvarchar](50) NOT NULL, --{delimiter_1} شناسه_ملی_خریدار
            [PostalCode] [nvarchar](50) NOT NULL, --{delimiter_1} کد_پستی_خریدار
            [BranchNumber] [nvarchar](50) NOT NULL, --{delimiter_1} کد_شعبه_خریدار
            [EconomicCode] [nvarchar](50) NOT NULL, --{delimiter_1} کد_اقتصادی_خریدار
            [IsActive] [tinyint] NOT NULL, --{delimiter_1} فعال_غیرفعال
            [Phone] [nvarchar](250) NOT NULL, --{delimiter_1} تلفن_ثابت_خریدار
            [Mobile] [nvarchar](250) NOT NULL, --{delimiter_1} موبایل_خریدار
            [Address] [nvarchar](250) NOT NULL, --{delimiter_1} آدرس_خریدار
            [Description] [nvarchar](250) NOT NULL, --{delimiter_1} توضیحات_خریدار
            [LastUpdateJalali] [nvarchar](20) NOT NULL, --{delimiter_1} زمان_تغییر_خریدار
            [UpdateBy] [bigint] NOT NULL, --{delimiter_1} کاربر_تغییر_خریدار
            [id] [bigint] IDENTITY(1,1) NOT NULL,
        CONSTRAINT [PK_Customers] PRIMARY KEY CLUSTERED
        (
            [id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[Goods](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [TaxSystemCode] [nvarchar](50) NOT NULL, --{delimiter_1} کد_دارایی_کالا
            [Description] [nvarchar](250) NOT NULL, --{delimiter_1} شرح_دارایی_کالا
            [GoodUnit] [bigint] NULL, --{delimiter_1} کلید_خارجی_واحد
            [TaxRate] [decimal](25, 8) NOT NULL, --{delimiter_1} نرخ_مالیات
            [UserDescription] [nvarchar](250) NOT NULL, --{delimiter_1} عنوان_کالا
            [UserCode] [nvarchar](50) NOT NULL, --{delimiter_1} کددلخواه_کالا
            [LastUpdateJalali] [nvarchar](20) NOT NULL, --{delimiter_1} زمان_تغییر_کالا
            [UpdateBy] [bigint] NOT NULL, --{delimiter_1} کاربر_تغییر_کالا
        CONSTRAINT [PK_goods] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[GoodUnits](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Name] [nvarchar](150) NOT NULL,  --{delimiter_1} عنوان_واحد
        CONSTRAINT [PK_GoodUnits] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]

        
        
        CREATE TABLE [dbo].[Invoices](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [TaxId] [nvarchar](50) NOT NULL, --{delimiter_1} شناسه_یکتای_صورتحساب
            [FactorNumber] [bigint] NOT NULL, --{delimiter_1} شماره_سریال_صورتحساب
            [CreateDateJalali] [nvarchar](20) NULL, --{delimiter_1} زمان_ارسال_به_دارایی
            [InvoiceType] [tinyint] NOT NULL, --{delimiter_1} نوع_صورتحساب
            [Pattern] [tinyint] NOT NULL, --{delimiter_1} الگو_صورتحساب
            [Subject] [tinyint] NOT NULL,--{delimiter_1} موضوع_صورتحساب
            [CustomerId] [bigint] NULL, --{delimiter_1} کلیدخارجی_خریدار
            [PaymentMethod] [tinyint] NOT NULL, --{delimiter_1} روش_پرداخت
            [Naghdi] [bigint] NOT NULL, --{delimiter_1} نقدی
            [Nesiye] [bigint] NOT NULL, --{delimiter_1} نسیه
            [ContractCode] [nvarchar](50) NOT NULL, --{delimiter_1} کد_قرارداد
            [DeliveryStatus] [tinyint] NOT NULL, --{delimiter_1} وضعیت_ارسال
            [DeliveryResult] [nvarchar](4000) NULL, --{delimiter_1} نتیجه_ارسال
            [Description] [nvarchar](500) NULL, --{delimiter_1} توضیحات_فاکتور
            [LastUpdateJalali] [nvarchar](20) NOT NULL, --{delimiter_1} زمان_تغییر_صورتحساب
            [UpdateBy] [bigint] NOT NULL, --{delimiter_1} کاربر_تغییر_صورتحساب
            [TotalDiscount] [bigint] NULL, --{delimiter_1} جمع_تخفیف_صورتحساب
            [TotalPrice] [bigint] NULL, --{delimiter_1} جمع_مبلغ_صورتحساب
            [TotalTax] [bigint] NULL, --{delimiter_1} جمع_مالیات_صورتحساب
            [NetValue] [bigint] NULL, --{delimiter_1} جمع_خالص_صورتحساب
            [ShowInList] [tinyint] NOT NULL, --{delimiter_1} موثر_در_محاسبه
            [CustomCode] [nvarchar](50) NOT NULL, --{delimiter_1} شماره_دستی_صورتحساب
            [SendDateJalali] [nvarchar](20) NOT NULL, --{delimiter_1}  تاریخ_صورتحساب 
        CONSTRAINT [PK_Invoices] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

        

        CREATE TABLE [dbo].[InvoiceItems](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [GoodId] [bigint] NOT NULL, --{delimiter_1} کلیدخارجی_کالا
            [InvoceId] [bigint] NOT NULL,--{delimiter_1} کلیدخارجی_صورتحساب
            [Quantity] [decimal](25, 8) NOT NULL, --{delimiter_1} تعداد_هرردیف_صورتحساب
            [TaxRate] [decimal](25, 8) NOT NULL, --{delimiter_1} درصد_مالیات_هرردیف_صورتحساب
            [UnitPrice] [decimal](25, 8) NOT NULL, {delimiter_1} قیمت_واحد_هرردیف_صورتحساب
            [Discount] [bigint] NOT NULL, --{delimiter_1} تخفیف_هرردیف_صورتحساب
            [Description] [nvarchar](250) NULL, --{delimiter_1} توضیحات_هرردیف_صورتحساب
            [LastUpdateJalali] [nvarchar](20) NOT NULL, --{delimiter_1} زمان_تغییر_هرردیف_صورتحساب
            [UpdateBy] [bigint] NOT NULL, --{delimiter_1} کاربر_تغییر_هرردیف_صورتحساب
            [TotalPrice] [bigint] NULL, --{delimiter_1} جمع_مبلغ_هرردیف_صورتحساب
            [TotalTax] [bigint] NULL, --{delimiter_1} مالیات_هرردیف_صورتحساب
            [NetValue] [bigint] NULL, --{delimiter_1} مبلغ_خالص_هرردیف_صورتحساب
        CONSTRAINT [PK_InvoiceItems] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[AccountGroups](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Title] [nvarchar](150) NOT NULL, --{delimiter_1} عنوان_حساب
            [Code] [int] NOT NULL, --{delimiter_1} کد_حساب
            [IsActive] [tinyint] NOT NULL, --{delimiter_1} وضعیت_حساب
            [Kind] [int] NOT NULL, --{delimiter_1} نوع_حساب
            [Nature] [int] NOT NULL, --{delimiter_1} ماهیت_حساب
        CONSTRAINT [PK_AccountGroups] PRIMARY KEY CLUSTERED
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[AccountingDocs](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [DocNo] [bigint] NOT NULL, --{delimiter_1} شماره_سند_حسابداری
            [CreationDateJalali] [nvarchar](50) NULL, --{delimiter_1} تاریخ_سند
            [Description] [nvarchar](250) NULL, --{delimiter_1} شرح_کلی_سند
            [TotalDebt] [decimal](18, 0) NULL, --{delimiter_1} جمع_بدهکار
            [Kind] [tinyint] NOT NULL, --{delimiter_1} نوع_سند
            [Status] [tinyint] NOT NULL, --{delimiter_1} وضعیت_سند
            [ApprovedBy] [bigint] NULL, --{delimiter_1} تایید_کننده_سند
            [ApprovalDateJalali] [nvarchar](50) NULL, --{delimiter_1} تاریخ_تایید_سند
            [TotalCredit] [decimal](18, 0) NULL, --{delimiter_1} جمع_بستانکاد
            [IsApproved] [tinyint] NOT NULL, --{delimiter_1} وضعیت_تایید
            [DailyNo] [int] NULL, --{delimiter_1} شماره_روزانه_سند
            [HasAttach] [bit] NOT NULL, --{delimiter_1} وضعیت_پیوست_سند
        CONSTRAINT [PK_AccountingDocs] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]
        Go

        CREATE TABLE [dbo].[DocItems](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [DocId] [bigint] NULL, --{delimiter_1} کلید_خارجی_سند
            [SubledgerId] [bigint] NULL, --{delimiter_1} کلید_خارجی_حساب_معین
            [TotalDept] [decimal](18, 0) NOT NULL, --{delimiter_1} مبلغ_بدهکار_ردیف_سند
            [Description] [nvarchar](250) NULL, --{delimiter_1} شرح_ردیف_سند
            [TafsilId1] [bigint] NULL, --{delimiter_1} کلید_خارجی_حساب_تفصیل_1
            [TafsilId2] [bigint] NULL, --{delimiter_1} کلید_خارجی_حساب_تفصیل_2
            [TafsilId3] [bigint] NULL, --{delimiter_1} کلید_خارجی_حساب_تفصیل_3
            [TafsilId4] [bigint] NULL, --{delimiter_1} کلید_خارجی_حساب_تفصیل_4
            [TotalCredit] [decimal](18, 0) NOT NULL, --{delimiter_1} جمع_بستانکار_ردیف_سند
        CONSTRAINT [PK_DocItems] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[Ledgers](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [Code] [int] NOT NULL, --{delimiter_1} کد_حساب_کل
            [GroupId] [bigint] NOT NULL, --{delimiter_1} کلید_خارجی_گروه_حساب
            [Title] [nvarchar](150) NOT NULL, --{delimiter_1} عنوان_حساب_کل
            [Kind] [int] NOT NULL, --{delimiter_1} نوع_حساب_کل
            [Nature] [int] NOT NULL, --{delimiter_1} ماهیت_حساب_کل
            [IsActive] [tinyint] NOT NULL, --{delimiter_1} وضعیت_حساب_کل
        CONSTRAINT [PK_Ledgers_1] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[SubLedgers](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Code] [int] NOT NULL, --{delimiter_1} کد_حساب_معین
            [Title] [nvarchar](150) NOT NULL, --{delimiter_1} عنوان_حساب_معین
            [LedgerId] [bigint] NOT NULL, --{delimiter_1} کلید_خازجی_حساب_کل
            [IsActive] [tinyint] NOT NULL, --{delimiter_1} وضعیت_حساب_معین
            [Nature] [int] NOT NULL, --{delimiter_1} ماهیت_حساب_معین
            [Kind] [int] NOT NULL, --{delimiter_1} نوع_حساب_معین
            [TafsilId1] [bigint] NULL, --{delimiter_1} کلید_خارجی_نوع_تفصیل_1
            [TafsilId2] [bigint] NULL, --{delimiter_1} کلید_خارجی_نوع_تفصیل_2
            [TafsilId3] [bigint] NULL, --{delimiter_1} کلید_خارجی_نوع_تفصیل_3
            [TafsilId4] [bigint] NULL, --{delimiter_1} کلید_خارجی_نوع_تفصیل_4
        CONSTRAINT [PK_SubLedgers] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]

        CREATE TABLE [dbo].[Tafsils](
            [Id] [bigint] IDENTITY(1,1) NOT NULL, 
            [Code] [int] NOT NULL, --{delimiter_1} کد_حساب_تفصیل
            [TafsilTypeId] [bigint] NOT NULL, --{delimiter_1} کلید_خارجی_نوع_تفصیل
            [Title] [nvarchar](150) NOT NULL, --{delimiter_1} عنوان_حساب_تفصیل
            [IsActive] [tinyint] NOT NULL, --{delimiter_1} وضعیت_حساب_تفصیل
            [Description] [nvarchar](500) NULL, --{delimiter_1} توضیحات_تکمیلی_حساب_تفصیل
            [CustomerId] [bigint] NULL, --{delimiter_1} کلید_خارجی_خریدار
        CONSTRAINT [PK_Tafsils] PRIMARY KEY CLUSTERED 
        (
            [Id] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
        ) ON [PRIMARY]


        CREATE TABLE [dbo].[TafsilTypes](
            [Id] [bigint] IDENTITY(1,1) NOT NULL,
            [Code] [int] NOT NULL, --{delimiter_1} کد_نوع_تفصیل
            [Title] [nvarchar](150) NOT NULL, --{delimiter_1} عنوان_نوع_تفصیل
            [IsSystem] [tinyint] NOT NULL, --{delimiter_1} وضعیت_نوع_تفصیل_سیستمی
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

Naming rules:
- Every column in the schema has:
  - a REAL column name (the actual SQL identifier in the database),
  - and a Persian label shown after {delimiter_1}. The Persian label is NOT a real column name.
- When writing SQL expressions, you MUST use only the REAL column names from the schema.
- You MUST assign a Persian alias (translation) to every selected field using AS in the SELECT list.

STRICT CONSTRAINTS (DO NOT VIOLATE):
- You must use only the real column names from the schema in every part of the SQL query.
- Persian text (Persian translations / labels / aliases) is NEVER allowed inside:
  SELECT expressions (before AS), JOIN conditions, WHERE, GROUP BY, ORDER BY, HAVING, or any SQL expression.
- Persian aliases may be used ONLY after AS in the SELECT list.
- If a Persian translation appears anywhere else in the query as a column reference (e.g. c.نام_خریدار, i.نقدی, etc.), the SQL query is INVALID and must NOT be generated.

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
        max_new_tokens=1024,
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
