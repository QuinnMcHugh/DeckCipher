from django.http import  HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cipher.cipher_utils as cipher_utils

def index(request):
	return render(request, 'cipher/index.html')

@csrf_exempt
def generate_key(request):
	return JsonResponse({ "key": cipher_utils.generate_random_key() }, safe=False)

@csrf_exempt
def cipher_message(request):
	action = request.POST.get("action").strip()
	key = request.POST.get("key").strip()
	input_text = request.POST.get("input").strip()

	if (not action) or (not key) or (not input_text):
		return JsonResponse({ "error": True, "output": "Malformed input: action, key, and input text are all required" }, safe=False)
	if not cipher_utils.is_valid_key(key):
		return JsonResponse({ "error": True, "output": "Malformed input: key is not a valid deck of cards" }, safe=False)

	if action.lower() == "encipher":
		output = cipher_utils.encipher(input_text, key)
	elif action.lower() == "decipher":
		output = cipher_utils.decipher(input_text, key)
	else:
		return JsonResponse({ "error": True, "output": "Malformed input: action must be either Encipher or Decipher" }, safe=False)

	return JsonResponse({ "output": output }, safe=False)

def more_detail(request):
	return render(request, 'cipher/more-detail.html')
