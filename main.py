from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional,Dict
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "dbname=aws_invoice user=aws_invoice_user password=oFsKPV03cSTIvRFwmkEiiJhnc99dNhxp host=dpg-cnu1hgda73kc73f5966g-a port=5432"

app = FastAPI()

# Allow CORS for all origins during development (replace "*" with your actual frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class Invoice(BaseModel):
    invoice_number: str
    bill_date: str
    due_date: str
    client_name: str
    client_address: str
    client_email: EmailStr
    client_phone: str
    supplier_name: str
    supplier_address: str
    supplier_email: EmailStr
    supplier_phone: str
    tax: float
    sub_total: float
    grand_total: float
    remark: Optional[str] = None
    image: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/invoices/")
async def create_invoice(invoice: Invoice):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    insert = f"""
        INSERT INTO "Employee_forms" (invoice_number, bill_date, due_date, client_name, client_address, client_email, client_phone, supplier_name, supplier_address, supplier_email, supplier_phone, tax, sub_total, grand_total, remark, image)
        VALUES ('{invoice.invoice_number}', '{invoice.bill_date}', '{invoice.due_date}', '{invoice.client_name}', '{invoice.client_address}', '{invoice.client_email}', '{invoice.client_phone}', '{invoice.supplier_name}',
                '{invoice.supplier_address}', '{invoice.supplier_email}', '{invoice.supplier_phone}', {invoice.tax}, {invoice.sub_total}, {invoice.grand_total}, '{invoice.remark}', '{invoice.image}')
    """

    cursor.execute(insert)
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "Invoice created"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)) -> Dict:
    return {
        "invoice_number": "141671",
        "bill_date": "2022-10-04",
        "due_date": "2022-11-04",
        "client_name": "Client Name",
        "client_address": "Client Address",
        "client_email": "client@example.com",
        "client_phone": "1234567890",
        "supplier_name": "Supplier Name",
        "supplier_address": "Supplier Address",
        "supplier_email": "supplier@example.com",
        "supplier_phone": "0987654321",
        "tax": 10.0,
        "sub_total": 100.0,
        "grand_total": 110.0,
        "remark": "Sample remark",
        "image": file.filename
    }


# {
#   "invoice_number": "141671",
#   "bill_date": "2022-10-04",
#   "due_date": "2022-11-04",
#   "client_name": "Client Name",
#   "client_address": "Client Address",
#   "client_email": "client@example.com",
#   "client_phone": "1234567890",
#   "supplier_name": "Supplier Name",
#   "supplier_address": "Supplier Address",
#   "supplier_email": "supplier@example.com",
#   "supplier_phone": "0987654321",
#   "tax": 10.0,
#   "sub_total": 100.0,
#   "grand_total": 110.0,
#   "remark": "Sample remark",
#   "image": "Sample image"
# }
