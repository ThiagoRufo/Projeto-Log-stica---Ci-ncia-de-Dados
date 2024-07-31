import discord
import pandas as pd
from discord.ext import commands

# Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot
TOKEN = 'XXXXXXXXX'

# Custo médio por milha náutica para cada tipo de navio
custo_combustivel_por_milha_nautica = {
    'carga_geral': 4.855992111683343,
    'frig': 5.796646759514053,
    'gran': 3.8267991945711004,
    'conteiner': 3.3705956296314517,
    'ro_ro': 2.4114616195945597
}

# Grupos de portos
portos_china = ['Xangai', 'Ningbo-Zhoushan', 'Shenzhen', 'Hong Kong', 'Qingdao', 'Guangzhou', 'Tianjin']
portos_europa = ['Roterdã', 'Hamburgo']

# Carregar dados
def carregar_dados():
    rotas_df = pd.read_csv('\\rotas.csv')
    portos_df = pd.read_csv('\\portos.csv')
    taxas_portuarias_df = pd.read_csv('\\taxas_portuarias.csv')
    navios = {
        'carga_geral': pd.read_csv('\\navio_carga_geral.csv'),
        'frig': pd.read_csv('\\navio_frigorifico.csv'),
        'gran': pd.read_csv('\\navio_graneleiro.csv'),
        'conteiner': pd.read_csv('\\navio_porta_conteiner.csv'),
        'ro_ro': pd.read_csv('\\navio_ro_ro.csv')
    }
    custos_medios_por_tipo_custo_por_navio = {
        'carga_geral': pd.read_csv('\\gcustos_medios_por_tipo_custo_por_navio_carga_geral.csv'),
        'frig': pd.read_csv('\\custos_medios_por_tipo_custo_por_navio_frigorifico.csv'),
        'gran': pd.read_csv('\\1custos_medios_por_tipo_de_custo_graneleiro.csv'),
        'conteiner': pd.read_csv('\custos_medios_por_tipo_custo_por_navio_porta_conteiner.csv'),
        'ro_ro': pd.read_csv('\\custos_medios_por_tipo_custo_por_navio_ro_ro.csv')
    }

    return rotas_df, portos_df, taxas_portuarias_df, navios, custos_medios_por_tipo_custo_por_navio

# Calcular distância total da rota
def calcular_distancia_total(rotas_df, portos):
    distancia_total = 0
    for i in range(len(portos) - 1):
        origem = portos[i]
        destino = portos[i+1]
        rota = rotas_df[(rotas_df['Porto_Origem'] == origem) & (rotas_df['Porto_Destino'] == destino)]
        if not rota.empty:
            distancia_total += rota['Distancia'].values[0]
    return distancia_total

# Calcular custos portuários
def calcular_custos_portuarios(taxas_portuarias_df, portos, carga):
    custo_total = 0
    for porto in portos:
        taxa = taxas_portuarias_df[taxas_portuarias_df['Porto'] == porto]
        if not taxa.empty:
            custo_total += taxa['Valor_Por_Navio'].values[0] + (taxa['Valor_Por_Tonelada'].values[0] * carga)
    return custo_total

# Calcular custos de operação dos navios
def calcular_custos_navios(tipo_navio, distancia_total, carga, custos_medios_por_tipo_custo_por_navio):
    custos_medios = custos_medios_por_tipo_custo_por_navio[tipo_navio]

    # Obter custo de combustível por milha náutica
    custo_combustivel_por_milha = custo_combustivel_por_milha_nautica.get(tipo_navio, 0)
    custo_combustivel_total = distancia_total * custo_combustivel_por_milha

    # Soma de custos médios operacionais fixos (manutenção, seguros, taxas portuárias)
    custo_fixo_total = custos_medios[custos_medios['Tipo de Custo'] == 'Manutenção']['Valor (USD)'].values[0] + \
                       custos_medios[custos_medios['Tipo de Custo'] == 'Seguros']['Valor (USD)'].values[0] + \
                       custos_medios[custos_medios['Tipo de Custo'] == 'Taxas Portuárias']['Valor (USD)'].values[0]

    custo_total_especifico = custo_combustivel_total + custo_fixo_total
    return custo_total_especifico, custo_combustivel_total

# Função principal do bot
def bot_transporte(portos, carga, tipo_navio_usuario):
    # Carregar dados
    rotas_df, portos_df, taxas_portuarias_df, navios, custos_medios_por_tipo_custo_por_navio = carregar_dados()

    # Mapear entrada do usuário para chaves corretas do dicionário
    tipos_navio_map = {
        'frig': 'frig',
        'gran': 'gran',
        'graneleiro': 'gran',
        'conteiner': 'conteiner',
        'container': 'conteiner',
        'ro_ro': 'ro_ro',
        'roro': 'ro_ro',
        'carga_geral': 'carga_geral',
        'geral': 'carga_geral'
    }

    tipo_navio_usuario = tipos_navio_map.get(tipo_navio_usuario, 'carga_geral')

    # Calcular distância total da rota
    distancia_total = calcular_distancia_total(rotas_df, portos)

    # Calcular custos portuários
    custos_portuarios = calcular_custos_portuarios(taxas_portuarias_df, portos, carga)

    # Calcular custos dos navios
    custo_navio_usuario, custo_combustivel_usuario = calcular_custos_navios(tipo_navio_usuario, distancia_total, carga, custos_medios_por_tipo_custo_por_navio)
    custo_navio_usuario += custos_portuarios

    custo_navio_carga_geral, custo_combustivel_carga_geral = calcular_custos_navios('carga_geral', distancia_total, carga, custos_medios_por_tipo_custo_por_navio)
    custo_navio_carga_geral += custos_portuarios

    # Comparar custos
    resultado = ""
    if custo_navio_usuario < custo_navio_carga_geral:
        resultado += f"O navio {tipo_navio_usuario} é mais barato do que o navio carga geral.\n"
    elif custo_navio_usuario > custo_navio_carga_geral:
        resultado += f"O navio {tipo_navio_usuario} é mais caro do que o navio carga geral.\n"
    else:
        resultado += f"O custo do navio {tipo_navio_usuario} é igual ao custo do navio carga geral.\n"

    resultado += f"Custo total do navio {tipo_navio_usuario}: {custo_navio_usuario:.2f} USD\n"
    resultado += f"Custo total do navio carga geral: {custo_navio_carga_geral:.2f} USD\n"
    resultado += f"Custo de combustível do navio {tipo_navio_usuario}: {custo_combustivel_usuario:.2f} USD\n"
    resultado += f"Custo de combustível do navio carga geral: {custo_combustivel_carga_geral:.2f} USD\n"

    # Comparar custos para portos na China ou Europa dependendo do destino
    porto_destino = portos[-1]
    if porto_destino in portos_china:
        resultado += f"\nCálculo dos custos portuários para cada porto na China:\n"
        melhor_porto = None
        menor_custo = float('inf')
        for porto in portos_china:
            custos_porto = calcular_custos_portuarios(taxas_portuarias_df, [porto], carga)
            resultado += f"Custo total no porto {porto}: {custos_porto:.2f} USD\n"
            if custos_porto < menor_custo:
                menor_custo = custos_porto
                melhor_porto = porto
        resultado += f"\nMelhor porto na China em termos de custo: {melhor_porto} com custo de {menor_custo:.2f} USD\n"
    elif porto_destino in portos_europa:
        resultado += f"\nCálculo dos custos portuários para portos na Europa:\n"
        for porto in portos_europa:
            custos_porto = calcular_custos_portuarios(taxas_portuarias_df, [porto], carga)
            resultado += f"Custo total no porto {porto}: {custos_porto:.2f} USD\n"

    return resultado

# Configurar o bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='transporte')
async def transporte(ctx, portos: str, carga: float, tipo_navio: str):
    try:
        portos_list = eval(portos)  # Converte string de entrada para lista
        resultado = bot_transporte(portos_list, carga, tipo_navio)
        await ctx.send(resultado)
    except Exception as e:
        await ctx.send(f"Erro ao calcular custos: {e}")

# Executar o bot
bot.run(TOKEN)
