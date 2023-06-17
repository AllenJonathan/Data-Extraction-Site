from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import PDFFileForm
from .extract_data import pdf_to_csv


def upload_pdf(request):
    if request.method == 'POST':
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_type = str(file).split('.')[1]
            file_bytes = file.read()
            data = pdf_to_csv(file_bytes, file_type)
            return render(request, 'display.html', {'data': data})
    else:
        form = PDFFileForm()
    return render(request, 'upload.html', {'form': form})

