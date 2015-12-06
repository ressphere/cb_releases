__author__ = 'user'
import slimit
import os
import glob
import settings
import rcssmin
import re
class minifier:

    #def check_is_in_string(self, srcText):
    #    if '"' in  srcText and '//' in srcText:
    #        opencurly_index =  srcText.indexOf('"')
    #        closecurly_index =  srcText.lastIndexOf('"')
    #        first_comment_index = srcText.indexOf('//')

    def custom_minify(self, srcText):
        onelineText = ''
        pattern1 = '//.*'
        pattern2 = '/\*(.*?)\*/'
        listofText = srcText.split('\n')


        for i in range(len(listofText)):
            #remove comment with //
            matchers = re.findall(pattern1, listofText[i])
            for matcher in matchers:
                if '"//"' not in listofText[i] and \
                                "https://" not in listofText[i] and "http://" not in listofText[i]:
                    listofText[i] = listofText[i].replace(matcher, '')
                    listofText[i] = listofText[i].replace('//', '')
            onelineText = onelineText + listofText[i].strip()
        #remove comment with /* */
        onelineText = onelineText.strip()
        matchers = re.findall(pattern2, onelineText)
        for matcher in matchers:
            onelineText = onelineText.replace(matcher, '')
            onelineText = onelineText.replace('/**/', '')
        return onelineText.strip()

    def minifyCSSProc(self, srcText):
        return rcssmin.cssmin(srcText, keep_bang_comments=True)

    def minifyJSProc(self , srcText):
        return self.custom_minify(srcText)
        #return slimit.minify(srcText, mangle=True, mangle_toplevel=True)


    def doProcessFiles(self, minifyProc, sourcePaths, header, destPath, minPath):
        print("Combining to %s and %s" % (destPath,minPath))
        f = None
        mf = None
        if destPath:
            f = open(destPath, 'w')
        try:

            for srcFile in sourcePaths:
                print(srcFile)
                with open(srcFile) as inputFile:
                    srcText = inputFile.read()
                    minText = minifyProc(srcText)
            if f:
                f.write(srcText)
            mf = open(minPath, 'w')
            if header:
                mf.write(header)
            mf.write(minText)
        finally:
            if f:
                f.close()
            if mf and not mf.closed:
                mf.close()

    def doJSMin(self,sourcePaths, header, destPath, minPath):
        return self.doProcessFiles(self.minifyJSProc, sourcePaths, header, destPath, minPath)

    def doCSSMin(self,sourcePaths, header, destPath, minPath):
        return self.doProcessFiles(self.minifyCSSProc, sourcePaths, header, destPath, minPath)

    def minify_string(self, release_folder):
        for css_path in settings.css_paths:
            folder = os.path.join(release_folder, css_path.strip('/')).replace('/', os.path.sep)
            for path in glob.glob("%s%s*"%(folder, os.sep)):
                if os.path.isfile(path) and '.css' in path.lower():
                    if ".min.css" not in path.lower():
                        self.doCSSMin([path], None, None, path)

        for js_path in settings.js_paths:
            folder = os.path.join(release_folder, js_path.strip('/')).replace('/', os.path.sep)
            for path in glob.glob("%s%s*"%(folder, os.sep)):
                if os.path.isfile(path) and '.js' in path.lower():
                    if ".min.js" not in path.lower():
                        self.doJSMin([path], None, None, path)

