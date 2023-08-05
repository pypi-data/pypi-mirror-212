import sympy as sp
from sympy.calculus.util import continuous_domain

def metodo_bissecao(funcao, inicio_intervalo, fim_intervalo, precisao_tipo = 'e1',
                        precisao = 1e-9, mostre_iteracoes = True, max_iter = 15):
    
    # a função é recebida no formato string e depois desse 'if' muda para objeto sympy
    # por isso, esse bloco só é executado uma vez
    if type(funcao) == str:
        
        global x
        global f_formatada
        global n_iter
        
        # função transformada de string para objeto sympy, inicializar contador de iterações
        f_formatada = sp.sympify(funcao)
        n_iter = 0
        x = sp.Symbol('x')
        
        # checagem de erro no tipo da precisão
        if precisao_tipo not in ['e1', 'e2']:
        
            raise ValueError("Precisão deve ser alguma dessas: %r." % ['e1', 'e2'])

    n_iter+=1
    
    # avaliar função nos dois extremos
    func_no_inicio, func_no_fim = [f_formatada.evalf(subs = {x: inicio_intervalo}), 
                                   f_formatada.evalf(subs = {x: fim_intervalo})]

    # uma raiz de uma função contínua só existe em um intervalo se o produto dos dois extremos for < 0
    if func_no_inicio * func_no_fim >= 0:
        
        raise ValueError("O produto dos valores da função nos extremos deve ser menor que zero.")    
    
    # estimativa da raiz
    # avaliar a função no ponto estimado
    estim = (inicio_intervalo + fim_intervalo) / 2
    f_estim = f_formatada.evalf(subs = {x: estim})
    
    # calcular o erro, conforme o tipo especificado
    erro = abs(f_estim) if precisao_tipo == 'e1' else abs(inicio_intervalo - fim_intervalo)
    
    # saber se a função chegou no máximo permitido de iterações sem atingir a precisão definida
    if n_iter == max_iter:
        
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = ({inicio_intervalo:.9f} + {fim_intervalo:.9f}) / 2 = {estim:.9f}, erro: {erro}')
        return print('Máximo de iterações atingido.')

    # mostrar passos intermediários, se o usuário tiver escolhido essa opção
    if mostre_iteracoes:
        
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = ({inicio_intervalo:.9f} + {fim_intervalo:.9f}) / 2 = {estim:.9f}, erro: {erro}')
        print()
    
    # interromper a função se o tiver superado a precisão desejada 
    if erro < precisao:
            
        resposta = f"A raiz aproximada de f(x) encontrada é {estim:.9f}, com {precisao_tipo} = {erro}"
            
        return print(resposta)
    
    # caso não tenha atingido a precisão, redefinir intervalo de procura da raiz e executar a função novamente
    # função trocar de sinal entre o início do intervalo anterior e a estimativa atual, redefinir intervalo
    elif f_estim * func_no_inicio < 0:
        
        novo_fim = estim
        metodo_bissecao(f_formatada, inicio_intervalo, novo_fim, precisao_tipo, 
                            precisao, mostre_iteracoes, max_iter)
    
    # caso a função troque de sinal entre a estimativa atual e o fim do intervalo anterior, redefinir intervalo
    # e reiniciar procura
    elif f_estim * func_no_fim < 0:
        
        novo_inicio = estim
        metodo_bissecao(f_formatada, novo_inicio, fim_intervalo, 
                            precisao_tipo, precisao, mostre_iteracoes, max_iter)  


# In[ ]:


def metodo_posicao_falsa(funcao, inicio_intervalo, fim_intervalo, precisao_tipo = 'e1',
                              precisao = 1e-9, mostre_iteracoes = True, max_iter = 10):

    # a função é recebida no formato string e depois desse 'if' muda para objeto sympy
    # por isso, esse bloco só é executado uma vez
    if type(funcao) == str:
        
        global x
        global f_formatada
        global n_iter
    
        # função transformada de string para objeto sympy
        # inicializar contador de iterações
        f_formatada = sp.sympify(funcao)
        n_iter = 0
        x = sp.Symbol('x')
        
        # checagem de erro no tipo da precisão        
        if precisao_tipo not in ['e1', 'e2']:
        
            raise ValueError("Precisão deve ser alguma dessas: %r." % ['e1', 'e2'])
            
    n_iter+=1
    
    # avaliar função nos dois extremos
    func_no_inicio, func_no_fim = [f_formatada.evalf(subs = {x: inicio_intervalo}), 
                                   f_formatada.evalf(subs = {x: fim_intervalo})]
    
    # uma raiz de uma função contínua só existe em um intervalo se o produto dos dois extremos for < 0    
    if func_no_inicio * func_no_fim >= 0:
        
        raise ValueError("O produto dos valores da função nos extremos deve ser menor que zero.")  
    
    # fazer estimativa da raiz
    # avaliar a função no ponto estimado
    f_a = func_no_inicio
    f_b = func_no_fim 
    estim = (inicio_intervalo*f_b - fim_intervalo*f_a)/(f_b - f_a)
    f_estim = f_formatada.evalf(subs = {x: estim})
    
    # calcular o erro, conforme o tipo especificado
    erro = abs(f_estim) if precisao_tipo == 'e1' else abs(inicio_intervalo - fim_intervalo)
    
    # saber se a função chegou no máximo permitido de iterações sem atingir a precisão definida
    if n_iter == max_iter:
            
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = ({inicio_intervalo:.9f}*{f_b:.9f} - {fim_intervalo:.9f}*{f_a:.9f})/({f_b:.9f} - {f_a:.9f}) = {estim:.9f}, erro: {erro}')
        return print('Máximo de iterações atingido.')
    
    # mostrar passos intermediários, se o usuário tiver escolhido essa opção
    if mostre_iteracoes is True:
            
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = ({inicio_intervalo:.9f}*{f_b:.9f} - {fim_intervalo:.9f}*{f_a:.9f})/({f_b:.9f} - {f_a:.9f}) = {estim:.9f}, erro: {erro}')
        print()
   
    # interromper a função se o tiver superado a precisão desejada 
    if erro < precisao:
            
        resposta = f"A raiz aproximada de f(x) encontrada é {estim:.9f}, com {precisao_tipo} = {erro}"
            
        return print(resposta)
    
    # caso não tenha atingido a precisão, redefinir intervalo de procura da raiz e executar a função novamente
    # função trocar de sinal entre o início do intervalo anterior e a estimativa atual, redefinir intervalo        
    elif f_estim * func_no_inicio < 0:
        novo_fim = estim
        metodo_posicao_falsa(f_formatada, inicio_intervalo, novo_fim, precisao_tipo, 
                                  precisao, mostre_iteracoes, max_iter)
        
    # caso a função troque de sinal entre a estimativa atual e o fim do intervalo anterior, redefinir intervalo
    # e reiniciar procura            
    elif f_estim * func_no_fim < 0:
        novo_inicio = estim
        metodo_posicao_falsa(f_formatada, novo_inicio, fim_intervalo, precisao_tipo,
                                  precisao, mostre_iteracoes, max_iter)  


# In[ ]:


def metodo_ponto_fixo(funcao, f_iter, inicio_intervalo, fim_intervalo, x0, precisao_tipo = 'e1',
                           precisao = 1e-6, mostre_iteracoes = True, max_iter = 10):

    # a função é recebida no formato string e depois desse 'if' muda para objeto sympy
    # por isso, esse bloco só é executado uma vez
    if type(funcao) == str:
        
        global x
        global f_formatada
        global n_iter
        global f_iter_formatada
        
        # função transformada de string para objeto sympy
        # inicializar contador de iterações
        # criação de variáveis para checagem das três condições de convergência, que só será feito uma vez
        x = sp.Symbol('x')
        n_iter = 0
        f_iter_formatada = sp.lambdify(x, f_iter)
        f_formatada = sp.lambdify(x, funcao)        
        intervalo = sp.Interval(inicio_intervalo, fim_intervalo)
        derivada_f = sp.diff(sp.sympify(f_iter), x)
        derivada_eh_continua = continuous_domain(derivada_f, x, intervalo) == intervalo
        f_eh_continua = continuous_domain(sp.sympify(funcao), x, intervalo) == intervalo
        imagem_derivada = sp.imageset(x,derivada_f, sp.Interval(inicio_intervalo,fim_intervalo))

        # cond1: satisfeita se a função e sua derivada forem contínuas no intervalo
        # cond2: satisfeita se a imagem da derivada estiver entre -1 e 1 por todo intervalo
        # cond3: satisfeita se a aproximação inicial estiver contida no intervalo
        cond1 = True if derivada_eh_continua and f_eh_continua else False     
        cond2 = True if imagem_derivada.start > -1 and imagem_derivada.end < 1 else False
        cond3 = sp.Contains(x0, intervalo)
        
        # exibir condição e mensagem de erro caso alguma condição não tiver sido satisfeita
        if not (cond1 and cond2 and cond3):
                                                 
            cond_n_satisfeitas = {"1": cond1, "2": cond2, "3": cond3}
            cond_codes = [key for key, value in cond_n_satisfeitas.items() if not value]
            
            raise ValueError(("Condição(ões) não satisfeita(s): " + ", ".join(["%s"] * len(cond_codes))) % tuple(cond_codes))
        
        # checagem de erro no tipo da precisão        
        if precisao_tipo not in ['e1', 'e2']:
        
            raise ValueError("Precisão deve ser alguma dessas: %r." % ['e1', 'e2'])
        
    n_iter+=1
    

    # fazer estimativa da raiz
    # avaliar a função no ponto estimado    
    estim = f_iter_formatada(x0)
    f_estim = f_formatada(estim)    

    # calcular o erro, conforme o tipo especificado    
    erro = abs(f_estim) if precisao_tipo == 'e1' else abs(estim - x0)
    
    # saber se a função chegou no máximo permitido de iterações sem atingir a precisão definida
    if n_iter == max_iter:
        
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = f_iter(x_estim_anterior) = {f_iter_formatada(x0):.9f}, erro: {erro}')
        return print('Máximo de iterações atingido.')
    
    # mostrar passos intermediários, se o usuário tiver escolhido essa opção
    if mostre_iteracoes is True:
        
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = f_iter(x_estim_anterior) = {f_iter_formatada(x0):.9f}, erro: {erro}')
        print()

    # interromper a função se o tiver superado a precisão desejada 
    if erro < precisao:
            
        resposta = f"A raiz aproximada de f(x) encontrada é {estim:.9f}, com {precisao_tipo} = {erro}"
            
        return print(resposta)
    
    # caso não tenha atingido a precisão desejada, nem o máximo de iterações permitidas, recomeçar o processo
    # atualizando a estimativa
    elif erro > precisao:
        
        metodo_ponto_fixo(f_formatada, f_iter_formatada, inicio_intervalo, fim_intervalo, estim, precisao_tipo,
                               precisao, mostre_iteracoes, max_iter)


# In[ ]:


def metodo_newton_raphson(funcao, inicio_intervalo, fim_intervalo, x0, precisao_tipo = 'e1',
                               precisao = 1e-9, mostre_iteracoes = True, max_iter = 10):
    
    # a função é recebida no formato string e depois desse 'if' muda para objeto sympy
    # por isso, esse bloco só é executado uma vez
    if type(funcao) == str:
        
        global x
        global f_formatada
        global n_iter
        global derivada_lambdify
        
        # função transformada de string para objeto sympy
        # inicializar contador de iterações
        # criação de variáveis para checagem das três condições de convergência, que só será feito uma vez
        x = sp.Symbol('x')
        n_iter = 0
        f_formatada = sp.lambdify(x, funcao)        
        intervalo = sp.Interval(inicio_intervalo, fim_intervalo)
        derivada_f = sp.diff(funcao, x)
        derivada_lambdify = sp.lambdify(x, derivada_f)
        derivada_segunda_f = sp.diff(funcao, x, 2)
        
        # as condições de convergência são apenas a continuidade da função e suas duas primeiras derivadas
        cond1 = continuous_domain(sp.sympify(funcao), x, intervalo) == intervalo
        cond2 = continuous_domain(derivada_f, x, intervalo) == intervalo
        cond3 = continuous_domain(derivada_segunda_f, x, intervalo) == intervalo
        
        # exibir condição e mensagem de erro caso alguma condição não tiver sido satisfeita
        if not (cond1 and cond2 and cond3):
                                                 
            cond_n_satisfeitas = {"1": cond1, "2": cond2, "3": cond3}
            cond_codes = [key for key, value in cond_n_satisfeitas.items() if not value]
            
            raise ValueError(("Condição(ões) não satisfeita(s): " + ", ".join(["%s"] * len(cond_codes))) % tuple(cond_codes))
        
        if precisao_tipo not in ['e1', 'e2']:
        
            raise ValueError("Precisão deve ser alguma dessas: %r." % ['e1', 'e2'])
        
    n_iter+=1
    
    # fazer estimativa da raiz
    # avaliar a função no ponto estimado
    estim = x0 - (f_formatada(x0)/derivada_lambdify(x0))
    f_estim = f_formatada(estim)    
    
    # checagem de erro no tipo da precisão        
    erro = abs(f_estim) if precisao_tipo == 'e1' else abs(estim - x0)
    
    # saber se a função chegou no máximo permitido de iterações sem atingir a precisão definida
    if n_iter == max_iter:
        
        print(f'Iteração nº {n_iter}:')
        print(f'x_estim = {x0:.9f} - ({f_formatada(x0):.9f}/{derivada_lambdify(x0):.9f}) = {estim:.9f}, erro: {erro}')
        return print('Máximo de iterações atingido.')
    
    # mostrar passos intermediários, se o usuário tiver escolhido essa opção
    if mostre_iteracoes is True:
        print(f'Iteração nº {n_iter}:')    
        print(f'x_estim = {x0:.9f} - ({f_formatada(x0):.9f}/{derivada_lambdify(x0):.9f}) = {estim:.9f}, erro: {erro}')
        print()

    # interromper a função se o tiver superado a precisão desejada 
    if erro < precisao:
            
        resposta = f"A raiz aproximada de f(x) encontrada é {estim:.9f}, com {precisao_tipo} = {erro}"
            
        return print(resposta)
        
    # caso não tenha atingido a precisão desejada, nem o máximo de iterações permitidas, recomeçar o processo
    # atualizando a estimativa
    elif erro > precisao:
        
        metodo_newton_raphson(f_formatada, inicio_intervalo, fim_intervalo, estim, precisao_tipo,
                               precisao, mostre_iteracoes, max_iter)


# In[ ]:


def metodo_secante(funcao, inicio_intervalo, fim_intervalo, x0, x1, precisao_tipo = 'e1',
                               precisao = 1e-9, mostre_iteracoes = True, max_iter = 10):
    
    # a função é recebida no formato string e depois desse 'if' muda para objeto sympy
    # por isso, esse bloco só é executado uma vez
    if type(funcao) == str:
        
        global x
        global f_formatada
        global n_iter
        global derivada_lambdify
        
        # função transformada de string para objeto sympy
        # inicializar contador de iterações
        # criação de variáveis para checagem das três condições de convergência, que só será feito uma vez
        x = sp.Symbol('x')
        n_iter = 0
        f_formatada = sp.lambdify(x, funcao)        
        intervalo = sp.Interval(inicio_intervalo, fim_intervalo)
        derivada_f = sp.diff(funcao, x)
        derivada_lambdify = sp.lambdify(x, derivada_f)
        derivada_segunda_f = sp.diff(funcao, x, 2)
        
        # as condições de convergência são apenas a continuidade da função e suas duas primeiras derivadas
        # igual às condições do método de Newton-Raphson
        cond1 = continuous_domain(sp.sympify(funcao), x, intervalo) == intervalo
        cond2 = continuous_domain(derivada_f, x, intervalo) == intervalo
        cond3 = continuous_domain(derivada_segunda_f, x, intervalo) == intervalo
        
        # exibir condição e mensagem de erro caso alguma condição não tiver sido satisfeita
        if not (cond1 and cond2 and cond3):
                                                 
            cond_n_satisfeitas = {"1": cond1, "2": cond2, "3": cond3}
            cond_codes = [key for key, value in cond_n_satisfeitas.items() if not value]
            
            raise ValueError(("Condição(ões) não satisfeita(s): " + ", ".join(["%s"] * len(cond_codes))) % tuple(cond_codes))
        
        if precisao_tipo not in ['e1', 'e2']:
        
            raise ValueError("Precisão deve ser alguma dessas: %r." % ['e1', 'e2'])
        
    n_iter+=1
    
    # fazer estimativa da raiz
    # avaliar a função no ponto estimado
    estim = (x0*f_formatada(x1) - x1*f_formatada(x0))/(f_formatada(x1) - f_formatada(x0))
    f_estim = f_formatada(estim)    
    
    # checagem de erro no tipo da precisão        
    erro = abs(f_estim) if precisao_tipo == 'e1' else abs(estim - x0)
    
    # saber se a função chegou no máximo permitido de iterações sem atingir a precisão definida
    if n_iter == max_iter:
        
        print(f'Iteração nº {n_iter}:')    
        print(f'x_estim = ({x0:.9f}*{f_formatada(x1):.9f} - {x1:.9f}*{f_formatada(x0):.9f})/({f_formatada(x1):.9f} - {f_formatada(x0):.9f}) = {estim:.9f}, erro = {erro}')
        return print('Máximo de iterações atingido.')
    
    # mostrar passos intermediários, se o usuário tiver escolhido essa opção
    if mostre_iteracoes is True:
        
        print(f'Iteração nº {n_iter}:')    
        print(f'x_estim = ({x0:.9f}*{f_formatada(x1):.9f} - {x1:.9f}*{f_formatada(x0):.9f})/({f_formatada(x1):.9f} - {f_formatada(x0):.9f}) = {estim:.9f}, erro = {erro}')
        print()

    # interromper a função se o tiver superado a precisão desejada 
    if erro < precisao:
            
        resposta = f"A raiz aproximada de f(x) encontrada é {estim:.9f}, com {precisao_tipo} = {erro}"
            
        return print(resposta)
        
    # caso não tenha atingido a precisão desejada, nem o máximo de iterações permitidas, recomeçar o processo
    # atualizando a estimativa
    elif erro > precisao:
        
        metodo_secante(f_formatada, inicio_intervalo, fim_intervalo, x1, estim, precisao_tipo,
                               precisao, mostre_iteracoes, max_iter)
