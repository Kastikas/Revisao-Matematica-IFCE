import timeit
from manage_mathdata import PDFParser

sample_text = """
Este é um texto de teste para avaliar a performance.
Temos palavras com hifens no fim da linha como alternati-
va e quantidades.
Além disso, temos gráfi  co, afi rmativa, fi guras e superfí cie.
uti lizado, uti lizada, uti lizados, uti lizadas, uti lizando.
disti nta, disti ntas, obti do, obti da, obti dos, obti das.
quanti dade, quanti dades, alternati vas, identi fi car, signi fi ca.
Múltiplas quebras
de linha

devem ser tratadas e o texto final
formatado.
"""

def run_benchmark():
    iterations = 10000

    # Warmup
    for _ in range(100):
        PDFParser.clean_text(sample_text)

    start_time = timeit.default_timer()
    for _ in range(iterations):
        PDFParser.clean_text(sample_text)
    end_time = timeit.default_timer()

    duration = end_time - start_time
    print(f"Executions: {iterations}")
    print(f"Total time: {duration:.4f} seconds")
    print(f"Time per iteration: {(duration / iterations) * 1000:.4f} ms")

if __name__ == "__main__":
    run_benchmark()
