class multipleFunctions:
    def Subfields():
        list1 = ['Machine Learning','Neural Networks','Vision', 'Robotics','Speech Processing','Natural Language Processing']
        print('Sub-fields in AI are:')
        for temp in list1:
            print(temp)
        return

    def OddEven():
        num = int(input('Enter a number:'))
        print('Enter a number:', num)
        if num%2 == 0:
            msg = 'Even'
        else:
            msg = 'Odd'

        print(num, 'is', msg, 'number')
        return  

    def Elegible():
        gender = input('Your Gender - (Male / Female:)')
        print('Your Gender - (Male / Female:)', gender)
        age = int(input('Your Age:'))
        print('Your Age:', age)

        if gender == 'Male':
            if age>=21:
                print('ELIGIBLE')
            else:
                print('NOT Eligible')
        elif gender == 'Female':
            if age>=18:
                print('ELIGIBLE')
            else:
                print('NOT Eligible')
        else:
            print('Invalid Input')
        return
    def percentage():

        m1 = int(input('Subject1 ='))
        print('Subject1=',m1)
        m2 = int(input('Subject2 ='))
        print('Subject2=',m2)
        m3 = int(input('Subject3 ='))
        print('Subject3=',m3)
        m4 = int(input('Subject4 ='))
        print('Subject4=',m4)
        m5 = int(input('Subject5 ='))
        print('Subject5=',m5)
        total = m1+m2+m3+m4+m5
        print('Total = ',total)
        perc = total/500 * 100
        print('Percentage = ',perc)
        return

    def triangle():
        height = int(input('Height for Area Calculation'))
        print('Height for Area Calculation', height)
        breadth = int(input('Breadth for Area Calculation'))
        print('Breadth for Area Calculation', breadth)

        Area = (height * breadth)/2
        print('Area of Triangle: ', Area)

        height1 = int(input('Height for Perimeter Calculation'))
        print('Height1 for Perimeter Calculation', height1)
        height2 = int(input('Height2 for Perimeter Calculation'))
        print('Height2 for Perimeter Calculation', height2)
        breadth = int(input('Breadth for Perimeter Calculation'))
        print('Breadth for Perimeter Calculation', breadth)

        Perimeter = height1 + height2 + breadth
        print('Perimeter of Triangle: ' , Perimeter)
        return
