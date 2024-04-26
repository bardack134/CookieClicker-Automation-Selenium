# import webdriver


from pprint import pprint
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import KEYS
from selenium.webdriver.common.keys import Keys


# Mantener el navegador abierto después de que el script ha sido ejecutado, y ampliar el navegador
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)


# Crear objeto webdriver para Chrome con las opciones configuradas
driver = webdriver.Chrome(options=chrome_options)

# Diccionario donde se guardarán los elementos encontrados
events_dictionary = {}


try:

    # Obtener página web
    driver.get("https://orteil.dashnet.org/cookieclicker/")


    # Esperar hasta que los elementos estén disponibles
    wait = WebDriverWait(driver, 5)
    
    
    #esperar que la pagina carge
    sleep(3)
    
    
    #aceptamos webcookies
    website_cookies = driver.find_element(By.CSS_SELECTOR, "a.cc_btn.cc_btn_accept_all")
    website_cookies.click()
       
    
    #escogiendo el idioma del juego kun y haciendo click
    lenguaje = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="langSelect-EN"]')))  
    lenguaje.click()
    
    
    # espero 5 segundos a que carge la pagina kun
    sleep(5)
    
    
    # encontrando el boton de cookies
    cookie_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sectionLeft #cookieAnchor #bigCookie')))  
    
    
    #NOTE: ENCONTREAR EL BOTON USANDO BYXPATH
    # cookie_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[15]/div[8]/button')))  
        
except Exception as err:
    
    # Imprimir un mensaje de error si ocurre una excepción
    print(f"El elemento no fue encontrado: {err}")  
        

else:
             
    #cada 5 segundos vamos a chequiar la tienda para los upgrades que estan disponibles
    check_time=time.time() + 5     
    
    
    # si el boton cookie fue encontrado
    while True:
        
        #cada 0.05 segundos se hara click a la galleta
        sleep(0.05)
        
        
        #click a la galleta
        cookie_button.click() 
        
        
        now_time=time.time()
        
        
        
        #chequiamos si el tiempo actual "esta en segundos UTC"  es mayor que nuestro check_time, que es el tiempo que determinamos para mirar los upgrades
        if  now_time> check_time:
            print('prueba')
            
            
            
            try:
                #NOTE:chequiamos la cantidad de monedas actuales
                cookies_number_element=driver.find_element(By.XPATH, '//*[@id="cookies"]')    
                
                
                #metodo para obtener el texto del elemento 
                cookies_number_text=cookies_number_element.text
                
                
                #queremos solo la parte numerica y quitar el texto 'cookies', usamos el metodo split() de string para lograrlo, devuelve una lista de la cadena
                cookies_number_list=cookies_number_text.split()
                
                
                cookies_number=cookies_number_list[0]
                
                
                # print(f"the cookies number is {cookies_number}")
                
                
            except Exception as err:
    
                # Imprimir un mensaje de error si ocurre una excepción
                print(f"the element 'cookies_number' was not found: {err}")             
            
            
            #NOTE: obteniendo Todos los  update products  disponibles, es decir aquellos que tienen ya la clase "enabled"            
            try:
                update_items = driver.find_elements(by=By.CSS_SELECTOR, value="div.product.enabled")
                # print(f"the update_items is {update_items}")
                
            
            #si no se encuentra o occurre un error    
            except Exception as err:

                # Imprimir un mensaje de error si ocurre una excepción
                print(f"the element 'update_items' was not found: {err}")  
              
            
            #si se encontro los update items    
            else:
                
                try:                    
                    #lista donde guardaremos los precios de los elementos actualizar
                    price_items_list=[]
                    
                    
                    #itirenamos sobre los updates products 
                    for item in update_items:
                        
                        #buscamos la linea en el web inspect que tiene el valor del precio, que es <span> class=price
                        price_item=item.find_element(by=By.CSS_SELECTOR, value="span.price")
                        price_items_list.append(price_item)
                        
                        
                    print(f"longitud lista 'price_items_list': {len(price_items_list)}")
                    
                    
                    #lista donde guardaremos los precios de los elementos 
                    price_list=[]
                    
                    
                    #obteniendo el precio de los elementos encontrados en price_items_list
                    for item in price_items_list:
                        
                        #tomamos el texto del elemento html que viene siendo el precio y le quitamos la coma
                        price=item.text.replace(',', '')
                        
                        
                        #puede pasar que price este vacio alintentar convertilo a entero, entonces genera error
                        try:
                            price_list.append(int(price))
                    

                        except:
                            pass
                    print(price_list)
                         
                    
                except Exception as err:

                    # Imprimir un mensaje de error si ocurre una excepción
                    print(f"the element 'price_item' was not found: {err}")                          
    
        
                #NOTE*: de los precios de los productos disponibles, buscaremos el mas caro
                if len(price_list)!=0:
                    
                    #precio mas alto dentro de nuestra lista de precios
                    max_price=max(price_list)
                

                    #obtenemos el indice dentro de la lista relacionado a ese precio maximo
                    max_price_indice=price_list.index(max_price)
                    
                    
                    #el indice del precio maximo en la lista de precios, viene siendo el mismo indice en la lista padre que es update_items
                    max_price_update_items=update_items[max_price_indice]
                    
                    
                    #hacemos click en esa actualizacion que viene siendo la mas cara
                    max_price_update_items.click()
                    
                    print(f"the most expencive upgrate selected is :  {max_price_update_items.text}")
                    
                    
        else:
            print("the is not bigger than check time")