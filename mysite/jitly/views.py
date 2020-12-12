from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import base64
import random, string
from jitly.models import Link
from string import ascii_letters

# 함수:특정 길이의 문자열 랜덤으로 생성
# len:결과 값 길이, characters:사용할 문자 리스트
def rand_str(len, characters):
    return "".join([random.choice(characters) for _ in range(len)])

# 함수:URL 입력 화면, Link 정보를 DB에 저장
def main(request):

    # POST 통신인 경우
    if request.method=='POST':
        # 1. Form 데이터 받아 옴
        # 입력된 original URL
        input_url=request.POST.get("input_url")
        # 자바스크립트에서 유효한 URL인지 검증한 결과 값
        hidden=request.POST.get("hidden_box")

        # DB에 있는 전체 Link 리스트를 출력
        links=Link.objects.all()
        print('가져오자고요...',links)

        # 2. 검사
        # URL이 유효하지 않다면, HTML 페이지로 이동
        if hidden=='wrong url':
            return render(request,'main.html',{'links':links})

        # 3. 입력된 URL이 기존 DB에 있는 지 확인
        link=Link.objects.filter(original=input_url)
        # 있으면 새로 암호를 만들지 않아도 됨
        if link:
            # 해당하는 DB를 불러옴
            result=Link.objects.get(original=input_url).encoded
            
            # localhost 사용
            return render(request, 'main.html',{'result':'http://127.0.0.1:8000/'+result,'links':links})

        # 4. 없으면 Short URL 새로 만들어야 함
        else :
            # DB에 URL 저장
            link=Link(
                original=request.POST.get("input_url")
            )
            link.save()
            # 인덱스 받기
            #object=(Link.objects.filter(original=input_url))
            #object.id
            link_object = Link.objects.get(original=input_url)
            id=link_object.id
            print("아이디",id)
            
            # 인덱스 인코딩
            result=encoded=base62(id)
            # db 반영
            # 수정하는 코드
            link=Link.objects.get(pk=id)
            link.encoded=result
            link.save()
            # result 결과 값 리턴
            return render(request, 'main.html',{'result':'http://127.0.0.1:8000/'+result,'links':links})
            
    # GET 통신인 경우
    else :
        # DB에 있는 전체 Link 리스트를 출력
        links=Link.objects.all()
        return render(request, 'main.html',{'links':links})

# Short를 Original로 리다이렉션 하는 함수
def show(request,short):
    # 1. db에서 short인 객체를 찾는다. 
    # 2. short에 해당하는 original 링크를 찾는다.
    # 3. original 링크로 리다이렉션 한다.
    link=Link.objects.get(encoded=short)
    return HttpResponseRedirect(link.original)

# DB에서 반환한 index를 Base62로 인코딩 하는 함수 
def base62(index): 
    result = "" 
    # Base62 인코딩의 기본이 되는 문자들 
    words=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
    while index % 62 > 0 or result == "":
        # index가 62인 경우에도 적용되기 위해 do-while 형식
        result = result + words[index % 62] 
        index = int(index / 62)
    print(result)
    return result
