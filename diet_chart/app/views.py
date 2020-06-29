from django.shortcuts import render
from app.models import Myfooddata
from pulp import *
import random

# Create your views here.


def Menu(request):
	
	Veg = Myfooddata.objects.filter(food_group="Vegetables")
	Grain = Myfooddata.objects.filter(food_group="Grains and Pasta")
	Fat = Myfooddata.objects.filter(food_group="Fats and Oils")
	Meat = Myfooddata.objects.filter(food_group="Meats")
	Dairy = Myfooddata.objects.filter(food_group="Dairy and Egg Products")
	data = {'Veg':Veg, 'Grain':Grain, 'Fat':Fat, 'Meat':Meat, 'Dairy':Dairy}
	
	return render(request, 'index.html', data)


def Pulp(request):

	# Process Protein, Fat and Carbohydrate requirement
	# We Know
	# 1gm protein = 4cal
	# 1gm fat = 9cal
	# 1gm carbohydrate = 4cal
	# Average calories for diabetic patient
	# 1300 calories
	# So i divided into three parts 30% for breakfast, 35% for lunch and 35% for dinner (calories).This is average ratio
	protein_cal = request.POST['pro_cal']
	fat_cal = request.POST['fat_cal']
	carbohydrate_cal = request.POST['car_cal']

	break_protein_cal = (30*int(protein_cal))/100
	break_fat_cal = (30*int(fat_cal))/100
	break_carbohydrate_cal = (30*int(carbohydrate_cal))/100
	
	break_protein_gm = (break_protein_cal/4)*10
	break_fat_gm = (break_fat_cal/9)*10
	break_carbohydrate_gm = (break_carbohydrate_cal/4)*10


	lunch_protein_cal = (35*int(protein_cal))/100
	lunch_fat_cal = (35*int(fat_cal))/100
	lunch_carbohydrate_cal = (35*int(carbohydrate_cal))/100

	lunch_protein_gm = (lunch_protein_cal/4)*10
	lunch_fat_gm = (lunch_fat_cal/9)*10
	lunch_carbohydrate_gm = (lunch_carbohydrate_cal/4)*10

	dinner_protein_cal = (35*int(protein_cal))/100
	dinner_fat_cal = (35*int(fat_cal))/100
	dinner_carbohydrate_cal = (35*int(carbohydrate_cal))/100

	dinner_protein_gm = (dinner_protein_cal/4)*10
	dinner_fat_gm = (dinner_fat_cal/9)*10
	dinner_carbohydrate_gm = (dinner_carbohydrate_cal/4)*10

	# Breakfast Menu

	# Create the 'breakfast' variable to contain the problem data
	breakfast = LpProblem("Breakfast_Menu",LpMinimize)
 	
	# Process request
	r = Myfooddata.objects.get(pk=request.POST['dairy_id'])

	# Variables diary are created with a lower limit of zero
	x1=LpVariable(r.name,0,None,LpInteger)
	
	# The objective function is added to 'breakfast' first
	breakfast += x1, "Total Cost of Ingredients per can"

	# The Three constraints are entered
	breakfast += x1 == 100, "PercentagesSum"
	breakfast += float(r.protein)*x1 >= break_protein_gm, "ProteinRequirement"
	breakfast += float(r.fat)*x1 >= break_fat_gm, "FatRequirement"
	breakfast += float(r.carbohydrate)*x1 >= break_carbohydrate_gm, "CarbohydrateRequirement"


	# The problem is solved using PuLP's choice of Solver
	breakfast.solve()



	# Let's choose two random lunch and dinner ingredients.
	new_id = [request.POST['veg_id'], request.POST['grain_id'], request.POST['fat_id'], request.POST['meat_id']]
	random.shuffle(new_id)
	

	# Lunch Menu

	# Create the 'breakfast' variable to contain the problem data
	lunch = LpProblem("Lunch_Menu",LpMinimize)
 	
	# Process request
	r1 = Myfooddata.objects.get(pk=new_id[0])
	r2 = Myfooddata.objects.get(pk=new_id[1])

	# Variables diary are created with a lower limit of zero
	x1 = LpVariable(r1.name,0,None,LpInteger)
	x2 = LpVariable(r2.name,0,None,LpInteger)
	
	# The objective function is added to 'breakfast' first
	lunch += x1 + x2, "Total Cost of Ingredients per can"

	# The Three constraints are entered
	lunch += x1 + x2 == 100, "PercentagesSum"
	lunch += float(r1.protein)*x1 + float(r2.protein)*x2 >= lunch_protein_gm, "ProteinRequirement"
	lunch += float(r1.fat)*x1 + float(r2.fat)*x2 >= lunch_fat_gm, "FatRequirement"
	lunch += float(r1.carbohydrate)*x1 + float(r2.carbohydrate)*x2 >= lunch_carbohydrate_gm, "CarbohydrateRequirement"


	# The problem is solved using PuLP's choice of Solver
	lunch.solve()


	# Dinner Menu

	# Create the 'breakfast' variable to contain the problem data
	dinner = LpProblem("Dinner_Menu",LpMinimize)
 	
	# Process request
	r1 = Myfooddata.objects.get(pk=new_id[2])
	r2 = Myfooddata.objects.get(pk=new_id[3])

	# Variables diary are created with a lower limit of zero
	x1 = LpVariable(r1.name,0,None,LpInteger)
	x2 = LpVariable(r2.name,0,None,LpInteger)
	
	# The objective function is added to 'breakfast' first
	dinner += x1 + x2, "Total Cost of Ingredients per can"

	# The Three constraints are entered
	dinner += x1 + x2 == 100, "PercentagesSum"
	dinner += float(r1.protein)*x1 + float(r2.protein)*x2 >= dinner_protein_gm, "ProteinRequirement"
	dinner += float(r1.fat)*x1 + float(r2.fat)*x2 >= dinner_fat_gm, "FatRequirement"
	dinner += float(r1.carbohydrate)*x1 + float(r2.carbohydrate)*x2 >= dinner_carbohydrate_gm, "CarbohydrateRequirement"


	# The problem is solved using PuLP's choice of Solver
	dinner.solve()

	data = {'breakfast':breakfast.variables, 'lunch': lunch.variables, 'dinner': dinner.variables}

	return render(request, 'menu.html', data)