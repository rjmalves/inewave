import inewave.newave as nw

adterm = nw.Adterm.read("./deck_newave_2024_08_inewave/adterm.dat")
print(adterm.despachos)

#agrint = nw.Agrint.read("./deck_newave_2024_08_inewave/agrint.dat")
#print(agrint.limites_agrupamentos)

arquivos = nw.Arquivos.read("./deck_newave_2024_08_inewave/arquivos.dat")
print(arquivos.arquivos)

#bid = nw.bid.read("./deck_newave_2024_08_inewave/bid.dat")

c_adic = nw.Cadic.read("./deck_newave_2024_08_inewave/c_adic.dat")
print(c_adic.cargas)

caso = nw.Caso.read("./deck_newave_2024_08_inewave/caso.dat")
print(caso.arquivos)

#cdefvar = nw.Cdefvar.read("./deck_newave_2024_08_inewave/cdefvar.dat")

clast = nw.Clast.read("./deck_newave_2024_08_inewave/clast.dat")
print(clast.usinas)

confhd = nw.Confhd.read("./deck_newave_2024_08_inewave/confhd.dat")
print(confhd.usinas)

conft = nw.Conft.read("./deck_newave_2024_08_inewave/conft.dat")
print(conft.usinas)

curva = nw.Curva.read("./deck_newave_2024_08_inewave/curva.dat")
print(curva.curva_seguranca)

cvar = nw.Cvar.read("./deck_newave_2024_08_inewave/cvar.dat")
print(cvar.alfa_variavel)

dger = nw.Dger.read("./deck_newave_2024_08_inewave/dger.dat")
print(dger.nome_caso)

#dsvagua = nw.Dsvagua.read("./deck_newave_2024_08_inewave/dsvagua.dat")
#print(dsvagua.desvios)

#elnino = nw.Elnino.read("./deck_newave_2024_08_inewave/elnino.dat")

#ensoaux = nw.Ensoaux.read("./deck_newave_2024_08_inewave/ensoaux.dat")

exph = nw.Exph.read("./deck_newave_2024_08_inewave/exph.dat")
print(exph.expansoes)

ghmin = nw.Ghmin.read("./deck_newave_2024_08_inewave/ghmin.dat")
print(ghmin.geracoes)

gtminpat = nw.Gtminpat.read("./deck_newave_2024_08_inewave/gtminpat.dat")
print(gtminpat.data)

hidr = nw.Hidr.read("./deck_newave_2024_08_inewave/hidr.dat")
print(hidr.cadastro)

itaipu = nw.Itaipu.read("./deck_newave_2024_08_inewave/itaipu.dat")
print(itaipu.data)

#loss = nw.Loss.read("./deck_newave_2024_08_inewave/loss.dat")

manutt = nw.Manutt.read("./deck_newave_2024_08_inewave/manutt.dat")
print(manutt.manutencoes)

modif = nw.Modif.read("./deck_newave_2024_08_inewave/modif.dat")
print(modif.data)

patamar = nw.Patamar.read("./deck_newave_2024_08_inewave/patamar.dat")
print(patamar.carga_patamares)

penalid = nw.Penalid.read("./deck_newave_2024_08_inewave/penalid.dat")
print(penalid.penalidades)

#postos = nw.Postos.read("./deck_newave_2024_08_inewave/postos.dat")

re = nw.Re.read("./deck_newave_2024_08_inewave/re.dat")
print(re.restricoes)

ree = nw.Ree.read("./deck_newave_2024_08_inewave/ree.dat")
print(ree.remocao_ficticias)

selcor = nw.Selcor.read("./deck_newave_2024_08_inewave/selcor.dat")
print(selcor.considera_cortes_da_propria_iteracao)

shist = nw.Shist.read("./deck_newave_2024_08_inewave/shist.dat")
print(shist.data)

sistema = nw.Sistema.read("./deck_newave_2024_08_inewave/sistema.dat")
print(sistema.data)

tecno = nw.Tecno.read("./deck_newave_2024_08_inewave/tecno.dat")
print(tecno.data)

term = nw.Term.read("./deck_newave_2024_08_inewave/term.dat")
print(term.usinas)

vazoes = nw.Vazoes.read("./deck_newave_2024_08_inewave/vazoes.dat")
print(vazoes.vazoes)

vazpast = nw.Vazpast.read("./deck_newave_2024_08_inewave/vazpast.dat")
print(vazpast.tendencia)
