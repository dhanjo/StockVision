from django.shortcuts import render
import subprocess
import time,os
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from pymongo import MongoClient


def home(request):
    return render(request, 'SV_App/FE_struct.html')


def run_mrf(request):
    return render(request,'SV_App/MRF.html')
def run_TM(request):
    return render(request,'SV_App/tata.html')
def run_JS(request):
    return render(request,'SV_App/Jindal.html')
def run_HD(request):
    return render(request,'SV_App/HDFC.html')            
def run_RL(request):
    return render(request,'SV_App/Rel.html')

#----------------------------------------------------------------------#

def fetch_mrf_data(request):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["AI"]  
    collection = db["Data_Stock"]  

    # Query the database
    mrf_data = collection.find_one({"Symbol": "MRF.NS"})  # Adjust the query as needed

    if mrf_data:
        # Remove MongoDB's ObjectId since it's not JSON serializable
        mrf_data["_id"] = str(mrf_data["_id"])
        return JsonResponse({"status": "success", "data": mrf_data})
    else:
        return JsonResponse({"status": "error", "message": "Data not found"})
    
def fetch_rel_data(request):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["AI"]  
    collection = db["Data_Stock"]  

    # Query the database
    rel_data = collection.find_one({"Symbol": "RELIANCE.BO"})  # Adjust the query as needed

    if rel_data:
        # Remove MongoDB's ObjectId since it's not JSON serializable
        rel_data["_id"] = str(rel_data["_id"])
        return JsonResponse({"status": "success", "data": rel_data})
    else:
        return JsonResponse({"status": "error", "message": "Data not found"})
    
def fetch_hdfc_data(request):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["AI"]  
    collection = db["Data_Stock"]  

    # Query the database
    hdfc_data = collection.find_one({"Symbol": "HDFCBANK.NS"})  # Adjust the query as needed

    if hdfc_data:
        # Remove MongoDB's ObjectId since it's not JSON serializable
        hdfc_data["_id"] = str(hdfc_data["_id"])
        return JsonResponse({"status": "success", "data": hdfc_data})
    else:
        return JsonResponse({"status": "error", "message": "Data not found"})

def fetch_tata_data(request):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["AI"]  
    collection = db["Data_Stock"]  

    # Query the database
    tata_data = collection.find_one({"Symbol": "TATAMOTORS.NS"})  # Adjust the query as needed

    if tata_data:
        # Remove MongoDB's ObjectId since it's not JSON serializable
        tata_data["_id"] = str(tata_data["_id"])
        return JsonResponse({"status": "success", "data": tata_data})
    else:
        return JsonResponse({"status": "error", "message": "Data not found"})
    
def fetch_jindal_data(request):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["AI"]  
    collection = db["Data_Stock"]  

    # Query the database
    jindal_data = collection.find_one({"Symbol": "JINDALSTEL.NS"})  # Adjust the query as needed

    if jindal_data:
        # Remove MongoDB's ObjectId since it's not JSON serializable
        jindal_data["_id"] = str(jindal_data["_id"])
        return JsonResponse({"status": "success", "data": jindal_data})
    else:
        return JsonResponse({"status": "error", "message": "Data not found"})