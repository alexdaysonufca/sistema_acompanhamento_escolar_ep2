"""
Funções utilitárias para validação de dados.
"""
import re
from datetime import datetime


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro.
    
    Args:
        cpf: CPF a validar (pode ter formatação ou não)
        
    Returns:
        True se CPF válido, False caso contrário
    """
    if not cpf:
        return False
    
    # Remove caracteres não numéricos
    numeros = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(numeros) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if numeros == numeros[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(numeros[i]) * (10 - i)
    primeiro_digito = (soma * 10 % 11) % 10
    
    # Calcula segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(numeros[i]) * (11 - i)
    segundo_digito = (soma * 10 % 11) % 10
    
    # Verifica se os dígitos calculados conferem
    return int(numeros[9]) == primeiro_digito and int(numeros[10]) == segundo_digito


def validar_email(email: str) -> bool:
    """
    Valida formato de email.
    
    Args:
        email: Email a validar
        
    Returns:
        True se email válido, False caso contrário
    """
    if not email:
        return False
    
    # Padrão básico: algo@dominio.extensão
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    email = email.strip().lower()
    
    if not re.match(padrao, email):
        return False
    
    # Verifica tamanhos
    if len(email) < 5 or len(email) > 254:
        return False
    
    # Verifica parte local (antes do @)
    local = email.split('@')[0]
    if len(local) > 64:
        return False
    
    return True


def normalizar_cpf(cpf: str) -> str:
    """
    Remove formatação do CPF, retornando apenas números.
    
    Args:
        cpf: CPF formatado ou não
        
    Returns:
        CPF com apenas dígitos
    """
    return re.sub(r'[^0-9]', '', cpf)


def formatar_cpf(cpf: str) -> str:
    """
    Formata CPF no padrão XXX.XXX.XXX-XX.
    
    Args:
        cpf: CPF apenas com dígitos
        
    Returns:
        CPF formatado
    """
    numeros = normalizar_cpf(cpf)
    if len(numeros) == 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    return cpf


def validar_ano_letivo(ano: int) -> bool:
    """
    Valida se ano é um ano letivo válido.
    
    Args:
        ano: Ano a validar
        
    Returns:
        True se ano válido (>= 2000 e até +2 anos no futuro)
    """
    if not isinstance(ano, int):
        return False
    
    ano_atual = datetime.now().year
    
    if ano < 2000:
        return False
    
    if ano > ano_atual + 2:
        return False
    
    return True
