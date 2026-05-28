import math
from flask import render_template, request

def calcular():
    try:
        num1 = float(request.form["num1"])
        operacao = request.form["operacao"]

        resultado = ""
        etapas = ""

    
        if operacao == "sqrt":
            if num1 < 0:
                resultado = "Erro"
                etapas = f"Não existe raiz real de números negativos ({num1})."
            else:
                resultado = round(math.sqrt(num1), 4)
                etapas = f"√{num1} = {resultado}"

     
        elif operacao == "bhaskara":
            num2_valor = request.form.get("num2", "").strip()
            num3_valor = request.form.get("num3", "").strip()
            
            if not num2_valor or not num3_valor:
                return render_template("calculadora.html", etapas="Para Bhaskara, informe os coeficientes b (num2) e c (num3).", resultados="")
            
            a = num1
            b = float(num2_valor)
            c = float(num3_valor)

            if a == 0:
                resultado = "Erro"
                etapas = "O coeficiente 'a' não pode ser zero em uma equação do 2º grau."
            else:
                delta = (b**2) - (4 * a * c)
                if delta < 0:
                    resultado = "Sem raízes reais"
                    etapas = f"Δ = {delta}. Como Delta é negativo, a equação não possui raízes reais."
                elif delta == 0:
                    x = -b / (2 * a)
                    resultado = f"x = {x}"
                    etapas = f"Δ = 0. A equação possui uma raiz real: x = {x}"
                else:
                    x1 = round((-b + math.sqrt(delta)) / (2 * a), 4)
                    x2 = round((-b - math.sqrt(delta)) / (2 * a), 4)
                    resultado = f"x' = {x1} | x'' = {x2}"
                    etapas = f"Δ = {delta}. Raízes encontradas: x' = {x1} e x'' = {x2}"

      
        else:
            num2_valor = request.form.get("num2", "").strip()
            
            if operacao == "log" and not num2_valor:
                num2_valor = "10"
                
            if not num2_valor:
                return render_template("calculadora.html", etapas="Informe o segundo número para esta operação.", resultados="")
            
            num2 = float(num2_valor)

            if operacao == "+":
                resultado = num1 + num2
                etapas = f"{num1} + {num2} = {resultado}"
            elif operacao == "-":
                resultado = num1 - num2
                etapas = f"{num1} - {num2} = {resultado}"
            elif operacao == "*":
                resultado = num1 * num2
                etapas = f"{num1} × {num2} = {resultado}"
            elif operacao == "/":
                if num2 == 0:
                    resultado = "Erro"
                    etapas = "Divisão por zero não é permitida."
                else:
                    resultado = round(num1 / num2, 4)
                    etapas = f"{num1} ÷ {num2} = {resultado}"
            elif operacao == "**":
                resultado = num1 ** num2
                etapas = f"{num1} ^ {num2} = {resultado}"
            elif operacao == "log":
                if num1 <= 0:
                    resultado = "Erro"
                    etapas = "O logaritmando (número) deve ser maior que zero."
                elif num2 <= 0 or num2 == 1:
                    resultado = "Erro"
                    etapas = "A base do logaritmo deve ser maior que zero e diferente de 1."
                else:
                    resultado = round(math.log(num1, num2), 4)
                    etapas = f"log base {num2} de {num1} = {resultado}"

        return render_template("calculadora.html", etapas=etapas, resultados=resultado)

    except ValueError:
        return render_template("calculadora.html", etapas="Erro nos dados enviados. Digite apenas números.", resultados="")