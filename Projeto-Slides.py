import cv2
import os

Caminho_Arquivo = '..\ProjetoSlides\img'
tamanho = 1500
largura = 1000
tempo_transicao = 2
tempo_imagem = 3
nome_janela="Image Slide Show"
formatos_suportados = ('.png', '.jpg', '.jpeg', '.bmp', '.dib', '.jpe', '.jp2', '.pgm', '.tiff', '.tif', '.ppm')
esc = 27
slides = 10
tamanho_minimo = 0
tamanho_maximo = 1

def passos(comeca, pausa, para):
	range = comeca
	while range < para:
		yield range
		range += pausa
	
def esperando_chave(segundos):
	estado = False	
	k = cv2.waitKey(int(segundos * 1000))
	
	if k == esc:  
		cv2.destroyWindow(nome_janela)
		estado = True

	return estado	
	

def carregando_caminho(caminho_imagem):
	
	_lista_imagens = []
	
	for nome_arquivo in os.listdir(caminho_imagem):
		
		_ler_imagens = os.path.join(caminho_imagem, nome_arquivo)
		
		if _ler_imagens.lower().endswith(formatos_suportados):
			_lista_imagens.append(_ler_imagens)
	
	return _lista_imagens


def carregar_imagem(caminho_ler, tamanho, altura): 	
	imagem = cv2.imread(caminho_ler,cv2.IMREAD_UNCHANGED)
	
	if imagem is not None:
		imagem_tamanho, imagem_largura = imagem.shape[:2]
	
		if imagem_largura > tamanho or imagem_tamanho > altura:
			interpolation = cv2.INTER_AREA
		else:
			interpolation = cv2.INTER_LINEAR
		
		_img_resized = cv2.resize(imagem, (tamanho, altura), interpolation)
	else:
		
		_img_resized = imagem
	return _img_resized	


lista_imagens = carregando_caminho(Caminho_Arquivo)

esperando_tempo_transicao = float (tempo_transicao) / slides
cv2.namedWindow(nome_janela,cv2.WINDOW_NORMAL)
primeira_imagem = None	

for imge_path in lista_imagens:
	
	if primeira_imagem is None:
		
		primeira_imagem = carregar_imagem(imge_path, tamanho, largura)
		
		cv2.imshow(nome_janela, primeira_imagem)

		if esperando_chave(tempo_imagem):
			break
		
		continue

	segunda_imagem = carregar_imagem(imge_path, tamanho, largura)

	for tamanho_Dois in passos(tamanho_minimo, float (tamanho_maximo)/slides, tamanho_maximo):
		
		tamanho_Um = tamanho_maximo - tamanho_Dois

		imagem_slide = cv2.addWeighted(primeira_imagem, tamanho_Um, segunda_imagem,tamanho_Dois, 0)

		cv2.imshow(nome_janela, imagem_slide)

		if esperando_chave(esperando_tempo_transicao):
			del lista_imagens[:]
			break

	if esperando_chave(tempo_imagem):
		break	
        
	primeira_imagem = segunda_imagem