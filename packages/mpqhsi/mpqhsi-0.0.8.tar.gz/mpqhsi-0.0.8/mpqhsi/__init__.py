import sys
import os
lib_path = (os.path.split(os.path.realpath(__file__))[0])
sys.path.append(lib_path)
import mpqcv
from My_HSI import *


def trans_Img(img):
    #####将高光图像数据标准化到0-255范围以供可见光显示#####
    img = trans_img(img)
    return img


def find_IJ(bin_img,key=255):#List:搜索数组，AimList:目标元素
    #####通过二值化图像寻找像素值为key的位置坐标并保存为列表#####
    i_j_list = find_ij(bin_img,key)
    return i_j_list

def read_Datacube(name1,name2):
    #####以datacube的形式读取高光谱数据#####
    data_cube = read_datacube(name1,name2)
    return data_cube

def read_Data_one_band(name1,name2,band=[80]):
    #####以灰度图像的形式读取高光谱数据，即单波段数据图像#####
    img_org = read_data_one_band(name1,name2,band)
    return img_org

def read_Data_one_sp(name1,name2,band=80,gre_thre=100,kernel = 10,iter1 = 0,iter2 = 0,key=0):
    #####通过该方法生成二值化图像及二值化图像像素值为key处所有高光谱数据的光谱数据并以列表形式显示#####
    bin_img, sp_list = read_data_one_sp(name1,name2,band,gre_thre,kernel,iter1,iter2,key)
    return bin_img,sp_list

def HSI_Read_one_band(name1,name2,band=[80]):
    #####通过该方法读取某个波段下高光谱图像数据，返回标准化后的图像#####
    img = HSI_read_one_band(name1,name2,band)
    return img

def HSI_Read_3bands(name1,name2,bands=[14,35,64]):
    #####通过该方法读取某个波段下高光谱图像数据，返回标准化后的图像#####
    img = HSI_read_3bands(name1,name2,bands)
    return img

def HSI_Show1band(img,band = [70],title = 'title'):
    #####通过该方法显示某个波段下高光谱图像数据标准化后的图像#####
    HSI_show_one_band(img,band,title)

def HSI_Show3bands(img,bands = [15,20,40],title = 'title'):
    #####通过该方法显示指定三个波段下高光谱图像数据标准化后的伪彩色图像#####
    HSI_show_3bands(img,bands,title)

def HSI_Show3D(img,bands=[15,50,70]):
    #####通过该方法显示高光谱数据立方块，指定波段为封面图像#####
    HSI_show_3D(img,bands)

def HSI_Savedir_graypic(in_path,out_oath,band=70):
    #####通过该方法将指定波段高光谱图像以灰度图像式保存到指定文件夹#####
    #此处原始数据类型需为.hdr和.cube##
    # eg:../../data/HSI/test_data/,最后有'/'
    HSI_savedir_graypic(in_path,out_oath,band)

def HSI_Savedir_rgbpic(in_path,out_oath,bands=[64,35,14]):
    #####通过该方法将指定波段高光谱图像以伪彩色图像式保存到指定文件夹#####
    # 此处原始数据类型需为.hdr和.cube##
    #eg:../../data/HSI/test_data/,最后有'/'
    HSI_savedir_rgbpic(in_path,out_oath,bands)


def HSI_Meandata_make(in_path,out_path,band=80,gre_thre=100):
    #####通过该方法将指定波段高光谱图像中目标区域平均光谱计算出来#####
    # 此处原始数据类型需为.hdr和.cube##
    result = HSI_meandata_make(in_path,out_path,band,gre_thre)
    return result

def HSI_get_splist_byclick(datacube, channal=3, bands=[10, 20, 30]):
    #####通过该方法可将鼠标点击位置光谱数据以dataframe的形式存在df中########
    df = get_splist_byclick(datacube, channal, bands)
    return df


if __name__ == '__main__':
    import mpqhsi as mhsi
    in_path = './test_data/'
    out_path = './'
    # result = HSI_meandata_make(in_path,out_path,band=80,thre=100)
    # result.to_csv('HSI_ROI_mean_data.csv',encoding='gb2312')

    # img = sp.envi.open('../../data/HSI/原始数据/正1-2.hdr', '../../data/HSI/原始数据/正1-2.cube')
    # # HSI_show_one_band(img,band=[70])
    # HSI_show_3D(img)
    # HSI_show_3bands(img,bands=[10,20,30])
    # HSI_savedirbgr_graypic('../../data/HSI/test_data/','./',band=80)
    # HSI_Savedir_rgbpic('./test_data/','./',bands=[15,35,64])
    # HSI_meandata_make('../../data/HSI/test_data/','./',gre_thre=100)
    # img = HSI_Read_one_band(r"D:\qiaozhiqi\Code\My_init\mpqhsi\mpqhsi-0.0.2\mpqhsi\test_data\反1-1.hdr",
    #                       r"D:\qiaozhiqi\Code\My_init\mpqhsi\mpqhsi-0.0.2\mpqhsi\test_data\反1-1.cube")

    # img = HSI_Read_3bands(r"D:\qiaozhiqi\Code\My_init\mpqhsi\mpqhsi-0.0.2\mpqhsi\test_data\反1-1.hdr",
    #                       r"D:\qiaozhiqi\Code\My_init\mpqhsi\mpqhsi-0.0.2\mpqhsi\test_data\反1-1.cube")

    name1 = r"D:\qiaozhiqi\Code\My_init\mpqhsi\mpqhsi-0.0.4\mpqhsi\test_data\baishao_2022-11-29_07-51-13\capture\baishao_2022-11-29_07-51-13.hdr"
    name2 = r"D:\qiaozhiqi\Code\My_init\mpqhsi\mpqhsi-0.0.4\mpqhsi\test_data\baishao_2022-11-29_07-51-13\capture\baishao_2022-11-29_07-51-13.raw"
    datacube = mhsi.read_Datacube(name1,name2)
    df = mhsi.HSI_get_splist_byclick(datacube)
    df.to_csv('aa.csv')
    # print(datacube[1,1,:].shape)
    # print(read_Data_one_band(name1,name2).shape)
    # bin = read_Data_one_sp(name1,name2,gre_thre=20)[0]
    # ijlist = read_Data_one_sp(name1,name2)[1]
    pic = HSI_Read_one_band(name1,name2)
    mpqcv.save_pic('a.png',pic)
    # print(len(ijlist))

    # print(read_Data_one_band(name1,name2,band=[10]).shape)
    # print(read_Data_one_band(name1,name2,band=10).shape)
    # print(type(read_Data_one_band(name1,name2,band=10)))
    # print(img.shape)
    # cv2.imshow('a',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


