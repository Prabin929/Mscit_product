from django.shortcuts import render
from .utils.model_saver import save_models
from django.shortcuts import render
from .models import StressData

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def add_stress_data(request):
    return render(request, 'stress_mgnt.html')


def stress_mgnt(request):
    return render(request,'stress_mgnt.html')

def stress_detect(request):
    return render(request,'stress_detect.html')



from django.shortcuts import render

def detect_stress(request):
    if request.method == 'POST':
        # Fetch input data from the form
        temperature = float(request.POST.get('mean_temperature'))
        eda = float(request.POST.get('mean_skin_conductance'))
        heart_rate = float(request.POST.get('mean_heart_rate'))

        # Use the predict_stress_level function
        stress_level = predict_stress_level(temperature, eda, heart_rate)

        # Determine stress level based on thresholds
        if temperature > high_stress_threshold['temperature'] or eda > high_stress_threshold['eda'] or heart_rate > high_stress_threshold['heart_rate']:
            stress_level = 'High Stress'
        elif temperature > medium_stress_threshold['temperature'] or eda > medium_stress_threshold['eda'] or heart_rate > medium_stress_threshold['heart_rate']:
            stress_level = 'Medium Stress'
        elif temperature > low_stress_threshold['temperature'] or eda > low_stress_threshold['eda'] or heart_rate > low_stress_threshold['heart_rate']:
            stress_level = 'Low Stress'
        else:
            stress_level = 'No Stress'

        # Save the stress level to the database
        stress_data = StressData(
            mean_temperature=temperature,
            mean_skin_conductance=eda,
            mean_heart_rate=heart_rate,
            stress_level=stress_level
        )
        stress_data.save()

        # Render the result in the template
        return render(request, 'result.html', {'stress_level': stress_level})

    # Render the initial form if not a POST request
    return render(request, 'stress_detect.html')


def stress_detection(request):
    if request.method == 'POST':
        # Assuming you have a form to collect input data
        # Retrieve input data from the form
        # ...

        # Load pre-trained models
        svm_model, dt_model = load_models()

        # Apply stress detection
        stress_result = detect_stress(svm_model, dt_model, input_data)

        # Save results to the database
        stress_data = StressData.objects.create(
            ID_Number=request.user.id,  # Assuming user is logged in
            mean_skin_conductance=input_data['mean_skin_conductance'],
            mean_heart_rate=input_data['mean_heart_rate'],
            mean_temperature=input_data['mean_temperature'],
            symptoms=input_data['symptoms'],
            stress_result=stress_result,
        )

        # Provide feedback based on stress_result
        feedback_message = "You are stressed. Here are some stress management tips."
        if stress_result == 'Not Stressed':
            feedback_message = "You are not stressed. Keep up the good work!"

        return render(request, 'stress_mgnt', {'feedback_message': feedback_message})

