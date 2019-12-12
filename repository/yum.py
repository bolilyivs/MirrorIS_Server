# coding=utf-8
import os, os.path
import shutil
import subprocess
import xml.dom.minidom

class Yum:
    def __init__(self):
        self.log = ""

    def subproc(self, str):
        try:
            self.log += subprocess.check_output(str, shell=True)
        except subprocess.CalledProcessError as e:
            return e
        return "success"


    def downloadFile(self, dirPath, dirName, linkFile):
        try:
            self.subproc("wget -P " + dirPath + dirName + " " + linkFile)
        except subprocess.CalledProcessError as e:
            return e
        return "success"


    def createStruct(self, dirPath, dirName):
        self.subproc("cd " + dirPath)
        self.subproc("mkdir downloads")
        self.subproc("mkdir " + dirName)


    def parse(self, dirPath, dirName, link):
        dom = xml.dom.minidom.parse(dirPath + dirName + "/repomd.xml")
        dom.normalize()
        nodes = dom.getElementsByTagName("location")
        for location in nodes:
            print(location.getAttribute('href'))
            Count = location.getAttribute('href').count('primary.xml.')
            if Count != 0:
                print(link)
                print(location.getAttribute('href').split('/')[1])
                self.downloadFile(dirPath, "downloads", link + "repodata/" + location.getAttribute('href').split('/')[1])
                self.parse2(dirPath, dirName, location.getAttribute('href').split('/')[1], link)
                break


    def parse2(self, dirPath, dirName, filePrimaryXml, link):
        # subproc("tar xvfz " + dirPath + "download" + "/" + filePrimaryXml)
        print(filePrimaryXml)
        print("gunzip " + dirPath + "downloads" + "/" + filePrimaryXml)

        self.subproc("gunzip " + dirPath + "downloads" + "/" + filePrimaryXml)

        dom = xml.dom.minidom.parse(dirPath + "downloads/" + filePrimaryXml.split('.')[0] + ".xml")
        dom.normalize()
        nodes = dom.getElementsByTagName("location")
        for location in nodes:
            print(location.getAttribute('href'))
            self.downloadFile(dirPath, "downloads", link + location.getAttribute('href'))
            self.subproc("tar xvfz " + dirPath + "downloads" + "/" + location.getAttribute('href').split('/')[1] + " -C " + dirPath + dirName)



    def run(self, dirPath, dirName, link):
        self.createStruct(dirPath, dirName)
        self.downloadFile(dirPath, dirName, link + "repodata/repomd.xml")
        self.downloadFile(dirPath, dirName, link + "repodata/repomd.xml.asc")
        self.parse(dirPath, dirName, link)
        return "success"


    def merge(self):
        try:
            self.log += subprocess.check_output(["cp", "-r", "usr1", "tusr"])
        except subprocess.CalledProcessError as e:
            return -2
        return 0


#run("/zstorage/yumi/", "testDir", "https://mirror.yandex.ru/centos/7.7.1908/os/x86_64/")
