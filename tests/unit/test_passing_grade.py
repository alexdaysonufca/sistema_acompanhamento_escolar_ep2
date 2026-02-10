"""
Teste da regra de aprovação: nota mínima 6.0.
Verifica a constante MEDIA_APROVACAO em ServicosDoAluno.
"""
from src.application.services import ServicosDoAluno


def test_media_aprovacao_eh_6():
    """A média mínima para aprovação deve ser 6.0."""
    assert ServicosDoAluno.MEDIA_APROVACAO == 6.0


def test_aprovado_com_nota_6():
    """Nota 6.0 aprova."""
    assert 6.0 >= ServicosDoAluno.MEDIA_APROVACAO


def test_reprovado_com_nota_5_9():
    """Nota 5.9 reprova."""
    assert 5.9 < ServicosDoAluno.MEDIA_APROVACAO
