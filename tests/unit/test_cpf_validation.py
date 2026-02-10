"""
Testes de validação de CPF.
Verifica o algoritmo de dígitos verificadores em src/utils.py.
"""
from src.utils import validar_cpf, normalizar_cpf, formatar_cpf


def test_cpf_valido_aceito():
    """CPFs com dígitos verificadores corretos são aceitos."""
    cpfs_validos = ["12345678909", "52998224725"]
    for cpf in cpfs_validos:
        assert validar_cpf(cpf) is True


def test_cpf_digitos_errados_rejeitado():
    """CPF com dígitos verificadores incorretos é rejeitado."""
    assert validar_cpf("12345678901") is False


def test_cpf_todos_iguais_rejeitado():
    """CPF com todos os dígitos iguais é rejeitado."""
    assert validar_cpf("11111111111") is False
    assert validar_cpf("00000000000") is False


def test_cpf_tamanho_errado_rejeitado():
    """CPF com menos ou mais de 11 dígitos é rejeitado."""
    assert validar_cpf("12345678") is False
    assert validar_cpf("123456789012") is False


def test_normalizar_cpf():
    """Remove pontos e traço."""
    assert normalizar_cpf("123.456.789-09") == "12345678909"


def test_formatar_cpf():
    """Formata como XXX.XXX.XXX-XX."""
    assert formatar_cpf("12345678909") == "123.456.789-09"
