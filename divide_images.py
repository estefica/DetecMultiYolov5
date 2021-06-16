import os, random, shutil, cv2
import lab_multis


def divide_img(imagen_faltantes,checI,val_test_check):
    #print('entre a dividir la imagen:')
    #print(checI)
    src_dir = '/content/random/images/'
    train_path = '/content/train/images/'
    dst_dir = ['/content/train/', '/content/valid/', '/content/test/']
    files_dst = ['images/', 'labels/']
    src_labels = '/content/random/labels/'
    menos_check=0
    for i in dst_dir:
        try:
            os.mkdir(i)
        except Exception as e:
            pass
            # print(e)

    for i in dst_dir:
        for j in files_dst:
            try:
                os.mkdir(i + j)
            except Exception as e:
                pass
                # print(e)

    numero_img_random = 7  # numero de imagenes random que escogere por cada imagen del dataset base
    data_setbase = os.listdir(train_path)  # LISTA DE IMAGENES TRAIN
    file_list = os.listdir(src_dir)  # Lista total de imgs creadas con el factor multiplicativo
    #print('Cantidad de donde escoger: ' + str(len(file_list)))

    # TRAIN DATASET
    nombre_imagen = []
    bandera_faltantes = int(len(file_list)) - numero_img_random
    iteraciones_faltantes = abs(bandera_faltantes)
    #print(f'!!! bandera faltantes:{bandera_faltantes}')

    
    
    if bandera_faltantes > 0 or imagen_faltantes == 0 or checI == 0 or val_test_check==1 :
        #print('entre a hay suficientes images')
        if val_test_check == 1 or menos_check==0 and checI==1:
          #print('TRAIN')
          for o_img in range(numero_img_random):
              a = random.choice(file_list)
              if a.endswith('.jpg'):
                  val_test_check +=1
                  shutil.move(src_dir + a, dst_dir[0] + files_dst[0] + a)
                  shutil.move(src_labels + a.replace('.jpg', '.txt'),
                              dst_dir[0] + files_dst[1] + a.replace('.jpg', '.txt'))
                  file_list.remove(a)
                  
              else:
                  #print('entre raaaroo')
                  numero_img_random += 1
        eval_n_images = 1
        test_n_images = random.choice([0, 1])
        division_imagenes = [eval_n_images, test_n_images]
        contador = 1    
          
        #print(f'Cantidad de donde escoger para eval : {len(os.listdir(src_dir))} ')
        if val_test_check > 1:
          #print('!!VAL Y TEST:')
          #print(f'val_test_check:{val_test_check}')
          try:
            if val_test_check<3:
              for i in range(eval_n_images):
                file_list = os.listdir(src_dir)
                a = random.choice(file_list)
                fn, ftext = os.path.splitext(a)
                #print('SOLO VAL')
                if os.path.exists(src_labels + fn + '.txt'):
                  val_test_check +=1
                  shutil.move(src_dir + a, '/content/valid/' + files_dst[0] + a)
                  shutil.move(src_labels + fn + '.txt', '/content/valid/' + files_dst[1] + fn + '.txt')
                  contador += 1
                  #print(fn)
            if val_test_check>2 and val_test_check<5:
              for i in range(test_n_images):
              
                file_list = os.listdir(src_dir)
                a = random.choice(file_list)
                fn, ftext = os.path.splitext(a)
                
                if os.path.exists(src_labels + fn + '.txt'):
                  #print('\n TEST')
                  
                  val_test_check +=1
                  shutil.move(src_dir + a, '/content/test/' + files_dst[0] + a)
                  shutil.move(src_labels + fn + '.txt', '/content/test/' + files_dst[1] + fn + '.txt')
                  #print(fn)
                  contador += 1
            bandera_faltantes= 1      
              

          except Exception as e:
              print(e)
          shutil.rmtree(src_dir)
          os.mkdir(src_dir)
          shutil.rmtree(src_labels)
          os.mkdir(src_labels)
          
    if bandera_faltantes <= 0 and imagen_faltantes != 0 and checI ==1:

        #print('entre a menos opcion')
        file_list = os.listdir(src_dir)
        # print(file_list)
        for i in range(len(file_list)):
            # print(f'entre al for:{i}')
            # print(file_list[i])
            fn, ftext = os.path.splitext(file_list[i])
            # print(fn)
            shutil.move(src_dir + fn + '.jpg', dst_dir[0] + files_dst[0] + fn + '.jpg')
            shutil.move(src_labels + fn + '.txt', dst_dir[0] + files_dst[1] + fn + '.txt')
            checI = 0
            val_test_check += 1
            menos_check = 1

        numero_img_random = iteraciones_faltantes
        shutil.rmtree(src_dir)
        os.mkdir(src_dir)
        shutil.rmtree(src_labels)
        os.mkdir(src_labels)
        
    
    return bandera_faltantes,checI,val_test_check


def escalado_inicial(path_imagenes, path_imagenes_t, path_save_files, path_save_filest):
    for f in os.listdir(path_imagenes):
        if f.endswith('.jpg'):

            fn, ftext = os.path.splitext(f)

            if os.path.exists(path_imagenes + fn + '.txt'):
                img = cv2.imread(path_imagenes + f'{fn}.jpg')

                imgResize = cv2.resize(img, (920, 720))

                cv2.imwrite(path_save_files + f'{fn}.jpg', imgResize)

                shutil.copy(path_imagenes_t + fn + '.txt', path_save_filest + f'{fn}.txt')

