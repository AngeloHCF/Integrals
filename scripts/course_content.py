"""Course worksheet source: 10 topics, 100 worked problems, and exact check specifications."""
TOPICS = [
    ('U-Substitution', 'Section 1.5'),
    ('Integration by Parts', 'Section 3.1'),
    ('Trig Integrals', 'Section 3.2'),
    ('Trigonometric Substitution', 'Section 3.3'),
    ('Partial Fractions', 'Section 3.4'),
    ('Summary of Integration Techniques', 'Mixed review'),
    ('Improper Integrals', 'Section 3.7'),
    ('Areas Between Curves', 'Section 2.1'),
    ('Determining Volumes by Slicing', 'Section 2.2'),
    ('Volumes of Revolution: Cylindrical Shells', 'Section 2.3'),
]
PROBLEMS = []

def add(topic, number, prompt, question, answer, method, steps, check):
    PROBLEMS.append(dict(
        id=f'ans{topic * 10 + number}', topic=TOPICS[topic][0], section=TOPICS[topic][1],
        difficulty='Medium' if number <= 7 else 'Hard' if number <= 9 else 'Tricky',
        prompt=prompt, question=question, answer=answer, method=method,
        steps=[dict(text=text, math=math) for text, math in steps], check=check,
    ))

def ant(topic, number, integrand, answer, method, steps, domain=''):
    add(topic, number, 'Find the indefinite integral.' + (' ' + domain if domain else ''),
        r'\int ' + integrand + r'\,dx', answer + ' + C', method, steps,
        dict(kind='antiderivative', integrand=integrand, primitive=answer))

def definite(topic, number, integrand, lower, upper, answer, method, steps, improper=False):
    add(topic, number,
        'Determine whether this improper integral converges. If it does, evaluate it.' if improper else 'Evaluate the definite integral exactly.',
        rf'\int_{{{lower}}}^{{{upper}}} {integrand}\,dx', answer, method, steps,
        dict(kind='integral', pieces=[dict(integrand=integrand, lower=lower, upper=upper)], improper=improper))

def geometry(topic, number, prompt, curves, answer, method, steps, pieces, variable='x'):
    add(topic, number, prompt, curves, answer, method, steps,
        dict(kind='integral', variable=variable, pieces=[dict(integrand=f, lower=a, upper=b) for f,a,b in pieces]))

# 1. U-substitution: include algebra before substitution and transformed limits.
ant(0,1,r'x^3\sqrt{x^2+1}',r'\frac{(x^2+1)^{5/2}}5-\frac{(x^2+1)^{3/2}}3','Substitution after rewriting',[
 ('Use the quadratic as the new variable, and rewrite the leftover square.',r'u=x^2+1,\quad du=2x\,dx,\quad x^2=u-1'),
 ('Replace every occurrence of the original variable before integrating.',r'I=\frac12\int(u-1)u^{1/2}\,du=\frac12\int(u^{3/2}-u^{1/2})\,du'),
 ('Apply the power rule and substitute back.',r'I=\frac{u^{5/2}}5-\frac{u^{3/2}}3+C,\quad u=x^2+1')])
ant(0,2,r'\frac{x\ln(1+x^2)}{1+x^2}',r'\frac14[\ln(1+x^2)]^2','Logarithmic substitution',[
 ('The derivative of the logarithm almost matches the remaining factor.',r'u=\ln(1+x^2),\quad du=\frac{2x}{1+x^2}\,dx'),
 ('Keep the factor of one half.',r'I=\frac12\int u\,du=\frac{u^2}{4}+C'),
 ('Restore the logarithm.',r'I=\frac14[\ln(1+x^2)]^2+C')])
ant(0,3,r'\frac{e^{2x}}{1+e^x}',r'e^x-\ln(1+e^x)','Substitution and division',[
 ('Use the exponential as the new variable; one exponential factor belongs to the differential.',r'u=e^x,\quad du=e^x\,dx,\quad I=\int\frac{u}{1+u}\,du'),
 ('Divide before integrating.',r'\frac{u}{1+u}=1-\frac1{1+u}'),
 ('Integrate and substitute back. The logarithm argument is positive.',r'I=u-\ln(1+u)+C=e^x-\ln(1+e^x)+C')])
ant(0,4,r'\frac{\sin x\cos x}{1+\sin^2x}',r'\frac12\ln(1+\sin^2x)','Substitute the denominator',[
 ('Differentiate the denominator.',r'u=1+\sin^2x,\quad du=2\sin x\cos x\,dx'),
 ('The integral becomes a logarithm.',r'I=\frac12\int\frac{du}{u}=\frac12\ln|u|+C'),
 ('Since the denominator is always positive, remove the absolute-value signs.',r'I=\frac12\ln(1+\sin^2x)+C')])
ant(0,5,r'\frac{(\ln x)^2}{x\sqrt{1+(\ln x)^3}}',r'\frac23\sqrt{1+(\ln x)^3}','Nested substitution',[
 ('Differentiate the full expression under the radical.',r'u=1+(\ln x)^3,\quad du=\frac{3(\ln x)^2}{x}\,dx'),
 ('Integrate the resulting negative half-power.',r'I=\frac13\int u^{-1/2}\,du=\frac23\sqrt u+C'),
 ('Restore the inner expression. The denominator requires a positive radicand.',r'I=\frac23\sqrt{1+(\ln x)^3}+C,\quad x>e^{-1}')])
definite(0,6,r'x(1+x^2)^3','0','1',r'\frac{15}{8}','Change the bounds with the variable',[
 ('Substitute and translate both bounds.',r'u=1+x^2,\quad du=2x\,dx,\quad x=0\Rightarrow u=1,\quad x=1\Rightarrow u=2'),
 ('Integrate in the new variable with the new bounds.',r'I=\frac12\int_1^2u^3\,du=\left[\frac{u^4}{8}\right]_1^2'),
 ('Evaluate upper minus lower.',r'I=\frac{16-1}{8}=\frac{15}{8}')])
ant(0,7,r'\frac{x+1}{\sqrt{x^2+2x+5}}',r'\sqrt{x^2+2x+5}','Match the inner derivative',[
 ('Notice that the numerator is half the derivative of the radicand.',r'u=x^2+2x+5,\quad du=2(x+1)\,dx'),
 ('Apply the power rule.',r'I=\frac12\int u^{-1/2}\,du=\sqrt u+C'),
 ('Substitute back; the radicand is positive for every real input.',r'I=\sqrt{x^2+2x+5}+C')])
ant(0,8,r'\frac1{\sqrt{x}(1+\sqrt{x})^2}',r'-\frac2{1+\sqrt x}','Substitute a radical',[
 ('Use the repeated radical expression as the variable.',r'u=1+\sqrt x,\quad du=\frac{dx}{2\sqrt x}'),
 ('The differential removes the extra radical in the denominator.',r'I=2\int u^{-2}\,du=-\frac2u+C'),
 ('Restore the variable and respect the original domain.',r'I=-\frac2{1+\sqrt x}+C,\quad x>0')])
ant(0,9,r'\frac{x^5}{(1+x^3)^2}',r'\frac13\ln|1+x^3|+\frac1{3(1+x^3)}','Substitution with a leftover factor',[
 ('Split the numerator into a square and a cube, then substitute.',r'u=1+x^3,\quad du=3x^2\,dx,\quad x^3=u-1'),
 ('Rewrite as two simple negative powers.',r'I=\frac13\int\frac{u-1}{u^2}\,du=\frac13\int(u^{-1}-u^{-2})\,du'),
 ('Integrate and replace the new variable.',r'I=\frac13\ln|u|+\frac1{3u}+C,\quad u=1+x^3')])
definite(0,10,r'x\sqrt{1+x^2}','-1','1','0','Check symmetry before computing',[
 ('The radical is even, while the factor outside it is odd.',r'f(-x)=-x\sqrt{1+x^2}=-f(x)'),
 ('Signed areas cancel on symmetric bounds; the integrand is continuous.',r'\int_{-1}^{1}f(x)\,dx=0'),
 ('A substitution gives an independent endpoint check.',r'F(x)=\frac13(1+x^2)^{3/2},\quad F(1)-F(-1)=0')])

# 2. Integration by parts.
ant(1,1,r'x^2\ln(2x)',r'\frac{x^3}{3}\ln(2x)-\frac{x^3}{9}','Differentiate the logarithm',[
 ('Choose parts so the logarithm becomes a reciprocal.',r'u=\ln(2x),\quad dv=x^2\,dx,\quad du=\frac{dx}{x},\quad v=\frac{x^3}{3}'),
 ('Apply integration by parts.',r'I=\frac{x^3}{3}\ln(2x)-\frac13\int x^2\,dx'),
 ('Integrate the remaining power.',r'I=\frac{x^3}{3}\ln(2x)-\frac{x^3}{9}+C')], 'Work on $x>0$.')
ant(1,2,r'x\arctan(2x)',r'\frac{4x^2+1}{8}\arctan(2x)-\frac x4','Parts followed by division',[
 ('Differentiate the inverse tangent and integrate the polynomial.',r'u=\arctan(2x),\quad dv=x\,dx,\quad du=\frac{2\,dx}{1+4x^2},\quad v=\frac{x^2}{2}'),
 ('Use division to simplify the remaining rational integral.',r'I=\frac{x^2}{2}\arctan(2x)-\frac14\int\left(1-\frac1{1+4x^2}\right)dx'),
 ('Integrate and combine the inverse-tangent terms.',r'I=\frac{4x^2+1}{8}\arctan(2x)-\frac x4+C')])
ant(1,3,r'x^2e^{-2x}',r'-e^{-2x}\left(\frac{x^2}{2}+\frac x2+\frac14\right)','Repeated integration by parts',[
 ('Differentiate the quadratic and integrate the exponential.',r'I=-\frac{x^2e^{-2x}}2+\int xe^{-2x}\,dx'),
 ('Use parts again on the remaining product.',r'\int xe^{-2x}\,dx=-\frac{xe^{-2x}}2-\frac{e^{-2x}}4'),
 ('Substitute and factor, then add one constant.',r'I=-e^{-2x}\left(\frac{x^2}{2}+\frac x2+\frac14\right)+C')])
ant(1,4,r'x\sin(3x)',r'-\frac{x\cos(3x)}3+\frac{\sin(3x)}9','Parts and chain-rule factors',[
 ('Differentiate the polynomial; include the frequency when integrating sine.',r'u=x,\quad dv=\sin(3x)\,dx,\quad v=-\frac{\cos(3x)}3'),
 ('Apply the formula.',r'I=-\frac{x\cos(3x)}3+\frac13\int\cos(3x)\,dx'),
 ('The remaining integration introduces another factor of one third.',r'I=-\frac{x\cos(3x)}3+\frac{\sin(3x)}9+C')])
ant(1,5,r'(\ln x)^2',r'x(\ln x)^2-2x\ln x+2x','Parts twice for logarithms',[
 ('Treat the integrand as a product with one.',r'u=(\ln x)^2,\quad dv=dx,\quad I=x(\ln x)^2-2\int\ln x\,dx'),
 ('Use parts on the remaining logarithm.',r'\int\ln x\,dx=x\ln x-x'),
 ('Substitute and simplify.',r'I=x(\ln x)^2-2x\ln x+2x+C')], 'Work on $x>0$.')
definite(1,6,r'xe^{2x}','0','1',r'\frac{e^2+1}{4}','Definite integration by parts',[
 ('Choose the polynomial as the part to differentiate.',r'u=x,\quad dv=e^{2x}\,dx,\quad v=\frac{e^{2x}}2'),
 ('Find an antiderivative before evaluating the endpoints.',r'F(x)=\frac{xe^{2x}}2-\frac{e^{2x}}4'),
 ('Subtract the lower endpoint carefully; it is negative.',r'I=F(1)-F(0)=\frac{e^2}{4}-\left(-\frac14\right)=\frac{e^2+1}{4}')])
ant(1,7,r'\arcsin x',r'x\arcsin x+\sqrt{1-x^2}','Inverse sine by parts',[
 ('Write the inverse sine as a product with one.',r'u=\arcsin x,\quad dv=dx,\quad I=x\arcsin x-\int\frac{x}{\sqrt{1-x^2}}\,dx'),
 ('Substitute in the remaining integral.',r'w=1-x^2,\quad dw=-2x\,dx,\quad \int\frac{x}{\sqrt{1-x^2}}\,dx=-\sqrt{1-x^2}'),
 ('Account for the minus sign from integration by parts.',r'I=x\arcsin x+\sqrt{1-x^2}+C')], 'Use $-1<x<1$ for the derivative calculation.')
ant(1,8,r'e^{3x}\sin(2x)',r'\frac{e^{3x}}{13}(3\sin(2x)-2\cos(2x))','Cycle back to the original integral',[
 ('Call the integral I and introduce the companion cosine integral J.',r'I=\frac{e^{3x}\sin(2x)}3-\frac23J,\quad J=\int e^{3x}\cos(2x)\,dx'),
 ('Integrate J by parts in the same way.',r'J=\frac{e^{3x}\cos(2x)}3+\frac23I'),
 ('Substitute and solve algebraically for I.',r'\frac{13}{9}I=\frac{e^{3x}\sin(2x)}3-\frac{2e^{3x}\cos(2x)}9'),
 ('Multiply by nine thirteenths and include the constant.',r'I=\frac{e^{3x}}{13}(3\sin(2x)-2\cos(2x))+C')])
ant(1,9,r'x^2\ln(1+x)',r'\frac{x^3+1}{3}\ln(1+x)-\frac{x^3}{9}+\frac{x^2}{6}-\frac x3','Parts and polynomial division',[
 ('Differentiate the logarithm and integrate the quadratic.',r'I=\frac{x^3}{3}\ln(1+x)-\frac13\int\frac{x^3}{x+1}\,dx'),
 ('Divide the cubic by the linear denominator.',r'\frac{x^3}{x+1}=x^2-x+1-\frac1{x+1}'),
 ('Integrate the polynomial and reciprocal terms.',r'I=\frac{x^3}{3}\ln(1+x)-\frac13\left(\frac{x^3}{3}-\frac{x^2}{2}+x-\ln(1+x)\right)+C'),
 ('Collect the logarithms and distribute the factor.',r'I=\frac{x^3+1}{3}\ln(1+x)-\frac{x^3}{9}+\frac{x^2}{6}-\frac x3+C')], 'Work on $x>-1$.')
ant(1,10,r'\frac{\ln x}{x^2}',r'-\frac{\ln x+1}{x}','A quotient can still require parts',[
 ('A substitution using the logarithm would leave an extra reciprocal. Use parts instead.',r'u=\ln x,\quad dv=x^{-2}\,dx,\quad du=\frac{dx}{x},\quad v=-\frac1x'),
 ('Track the two minus signs in the formula.',r'I=-\frac{\ln x}{x}+\int x^{-2}\,dx'),
 ('Integrate and combine the two terms.',r'I=-\frac{\ln x}{x}-\frac1x+C=-\frac{\ln x+1}{x}+C')], 'Work on $x>0$.')

# 3. Trigonometric integrals.
ant(2,1,r'\sin^3x\cos^4x',r'\frac{\cos^7x}{7}-\frac{\cos^5x}{5}','Save one sine factor',[
 ('Use the odd sine power to form a differential.',r'\sin^3x\cos^4x=(1-\cos^2x)\cos^4x\sin x'),
 ('Substitute for cosine and distribute the minus sign.',r'u=\cos x,\quad I=-\int(1-u^2)u^4\,du=\int(u^6-u^4)\,du'),
 ('Integrate and restore cosine.',r'I=\frac{u^7}{7}-\frac{u^5}{5}+C,\quad u=\cos x')])
ant(2,2,r'\sin^4x\cos^3x',r'\frac{\sin^5x}{5}-\frac{\sin^7x}{7}','Save one cosine factor',[
 ('Convert the even part of the cosine power to sine.',r'\sin^4x\cos^3x=\sin^4x(1-\sin^2x)\cos x'),
 ('Use sine as the variable.',r'u=\sin x,\quad I=\int(u^4-u^6)\,du'),
 ('Apply the power rule and substitute back.',r'I=\frac{\sin^5x}{5}-\frac{\sin^7x}{7}+C')])
ant(2,3,r'\tan^4x\sec^2x',r'\frac{\tan^5x}{5}','Tangent substitution',[
 ('Recognize the derivative of tangent.',r'u=\tan x,\quad du=\sec^2x\,dx'),
 ('Integrate the fourth power.',r'I=\int u^4\,du=\frac{u^5}{5}+C'),
 ('Replace the variable with tangent.',r'I=\frac{\tan^5x}{5}+C')])
ant(2,4,r'\sec^4x',r'\tan x+\frac{\tan^3x}{3}','Save a secant-squared factor',[
 ('Use the Pythagorean identity on one pair of secant factors.',r'\sec^4x=(1+\tan^2x)\sec^2x'),
 ('Substitute tangent.',r'u=\tan x,\quad I=\int(1+u^2)\,du'),
 ('Integrate the polynomial.',r'I=\tan x+\frac{\tan^3x}{3}+C')])
ant(2,5,r'\sin^2(3x)\cos^2(3x)',r'\frac x8-\frac{\sin(12x)}{96}','Double-angle and power reduction',[
 ('Combine the product using the double-angle formula.',r'\sin^2(3x)\cos^2(3x)=\frac14\sin^2(6x)'),
 ('Reduce the remaining square.',r'\frac14\sin^2(6x)=\frac18(1-\cos(12x))'),
 ('Integrate, dividing by twelve in the sine term.',r'I=\frac x8-\frac{\sin(12x)}{96}+C')])
ant(2,6,r'\sin(4x)\cos x',r'-\frac{\cos(5x)}{10}-\frac{\cos(3x)}6','Product to sum',[
 ('The angles differ, so use the product-to-sum identity.',r'\sin(4x)\cos x=\frac12(\sin(5x)+\sin(3x))'),
 ('Integrate each sine with its own frequency.',r'I=\frac12\left(-\frac{\cos(5x)}5-\frac{\cos(3x)}3\right)+C'),
 ('Distribute the factor of one half.',r'I=-\frac{\cos(5x)}{10}-\frac{\cos(3x)}6+C')])
ant(2,7,r'\tan^2x',r'\tan x-x','Rewrite before substituting',[
 ('There is no secant-squared differential yet; use an identity.',r'\tan^2x=\sec^2x-1'),
 ('Separate into two familiar integrals.',r'I=\int\sec^2x\,dx-\int1\,dx'),
 ('Integrate term by term.',r'I=\tan x-x+C')])
ant(2,8,r'\sec^5x',r'\frac{\sec^3x\tan x}{4}+\frac38\sec x\tan x+\frac38\ln|\sec x+\tan x|','Derive a reduction with parts',[
 ('Write the integrand as a cube times a secant square and integrate by parts.',r'u=\sec^3x,\quad dv=\sec^2x\,dx,\quad I=\sec^3x\tan x-3\int\sec^3x\tan^2x\,dx'),
 ('Replace tangent squared and move the original integral to the left.',r'4I=\sec^3x\tan x+3J,\quad J=\int\sec^3x\,dx'),
 ('Apply the same parts idea to J; use the standard secant logarithm.',r'2J=\sec x\tan x+\ln|\sec x+\tan x|'),
 ('Substitute J and divide by four.',r'I=\frac{\sec^3x\tan x}{4}+\frac38\sec x\tan x+\frac38\ln|\sec x+\tan x|+C')])
ant(2,9,r'\sin^4x\cos^2x',r'\frac{x}{16}-\frac{\sin(2x)}{64}-\frac{\sin(4x)}{64}+\frac{\sin(6x)}{192}','Reduce multiple even powers',[
 ('Set a temporary abbreviation and apply both half-angle identities.',r'c=\cos(2x),\quad \sin^4x\cos^2x=\frac18(1-c)^2(1+c)=\frac18(1-c-c^2+c^3)'),
 ('Use the square and triple-angle identities to reduce all powers.',r'\sin^4x\cos^2x=\frac1{16}-\frac{\cos(2x)}{32}-\frac{\cos(4x)}{16}+\frac{\cos(6x)}{32}'),
 ('Integrate each cosine with its frequency factor.',r'I=\frac{x}{16}-\frac{\sin(2x)}{64}-\frac{\sin(4x)}{64}+\frac{\sin(6x)}{192}+C')])
definite(2,10,r'\sin^3x\cos x','0',r'\pi','0','Equal transformed endpoints',[
 ('The cosine factor changes sign; the signed integral need not be positive.',r'u=\sin x,\quad du=\cos x\,dx'),
 ('Find an antiderivative in the original variable.',r'F(x)=\frac14\sin^4x'),
 ('Both endpoint values vanish. This is a signed integral, not the total area.',r'I=F(\pi)-F(0)=0')])

# 4. Trigonometric substitution, with explicit branches.
ant(3,1,r'\frac1{\sqrt{x^2+4}}',r'\ln|x+\sqrt{x^2+4}|','Tangent substitution',[
 ('Use tangent for a sum of squares and choose a positive secant branch.',r'x=2\tan\theta,\quad -\pi/2<\theta<\pi/2,\quad dx=2\sec^2\theta\,d\theta'),
 ('Simplify the radical and integrate secant.',r'\sqrt{x^2+4}=2\sec\theta,\quad I=\int\sec\theta\,d\theta=\ln|\sec\theta+\tan\theta|+C'),
 ('Substitute back; the constant logarithm of two is absorbed into C.',r'I=\ln|x+\sqrt{x^2+4}|+C')])
ant(3,2,r'\frac{x^2}{\sqrt{16-x^2}}',r'8\arcsin(x/4)-\frac x2\sqrt{16-x^2}','Sine substitution and power reduction',[
 ('Choose the branch with positive cosine.',r'x=4\sin\theta,\quad -\pi/2<\theta<\pi/2,\quad I=16\int\sin^2\theta\,d\theta'),
 ('Reduce the square and integrate.',r'I=8\theta-4\sin(2\theta)+C'),
 ('Use the double-angle relation to return to x.',r'\theta=\arcsin(x/4),\quad \sin(2\theta)=\frac{x\sqrt{16-x^2}}8')])
ant(3,3,r'\frac{\sqrt{25-x^2}}{x^2}',r'-\frac{\sqrt{25-x^2}}x-\arcsin(x/5)','Sine substitution leading to cotangent',[
 ('Choose sine and translate the differential and radical.',r'x=5\sin\theta,\quad \sqrt{25-x^2}=5\cos\theta,\quad dx=5\cos\theta\,d\theta'),
 ('The quotient becomes cotangent squared.',r'I=\int\cot^2\theta\,d\theta=\int(\csc^2\theta-1)\,d\theta=-\cot\theta-\theta+C'),
 ('Restore x on either side of zero.',r'\cot\theta=\frac{\sqrt{25-x^2}}x,\quad \theta=\arcsin(x/5)')], 'Assume $0<|x|<5$.')
ant(3,4,r'\frac1{(x^2+9)^{3/2}}',r'\frac{x}{9\sqrt{x^2+9}}','Tangent substitution',[
 ('Use tangent with positive secant.',r'x=3\tan\theta,\quad dx=3\sec^2\theta\,d\theta,\quad (x^2+9)^{3/2}=27\sec^3\theta'),
 ('Cancel powers and integrate cosine.',r'I=\frac19\int\cos\theta\,d\theta=\frac19\sin\theta+C'),
 ('Use the triangle relation to recover x.',r'\sin\theta=\frac{x}{\sqrt{x^2+9}},\quad I=\frac{x}{9\sqrt{x^2+9}}+C')])
ant(3,5,r'\frac{\sqrt{x^2-9}}x',r'\sqrt{x^2-9}-3\arctan\left(\frac{\sqrt{x^2-9}}3\right)','Secant substitution',[
 ('On the specified positive branch, use secant.',r'x=3\sec\theta,\quad 0<\theta<\pi/2,\quad \sqrt{x^2-9}=3\tan\theta'),
 ('Simplify the transformed integral using a Pythagorean identity.',r'I=3\int\tan^2\theta\,d\theta=3\tan\theta-3\theta+C'),
 ('Recover the angle with inverse tangent.',r'3\tan\theta=\sqrt{x^2-9},\quad \theta=\arctan\left(\frac{\sqrt{x^2-9}}3\right)')], 'Use $x>3$.')
definite(3,6,r'\sqrt{4-x^2}','0','2',r'\pi','Sine substitution with bounds',[
 ('Convert both the differential and the interval.',r'x=2\sin\theta,\quad x=0\Rightarrow\theta=0,\quad x=2\Rightarrow\theta=\pi/2'),
 ('Apply the cosine-square identity.',r'I=4\int_0^{\pi/2}\cos^2\theta\,d\theta=\left[2\theta+\sin(2\theta)\right]_0^{\pi/2}'),
 ('Evaluate; this agrees with the area of a quarter-circle of radius two.',r'I=\pi')])
ant(3,7,r'\frac1{(4-x^2)^{3/2}}',r'\frac{x}{4\sqrt{4-x^2}}','Sine substitution leading to secant squared',[
 ('Use the positive-cosine branch of sine substitution.',r'x=2\sin\theta,\quad dx=2\cos\theta\,d\theta,\quad (4-x^2)^{3/2}=8\cos^3\theta'),
 ('Simplify and integrate.',r'I=\frac14\int\sec^2\theta\,d\theta=\frac14\tan\theta+C'),
 ('Translate tangent back to x.',r'\tan\theta=\frac{x}{\sqrt{4-x^2}},\quad I=\frac{x}{4\sqrt{4-x^2}}+C')], 'Assume $|x|<2$.')
ant(3,8,r'\frac{x^2}{(x^2+4)^{5/2}}',r'\frac{x^3}{12(x^2+4)^{3/2}}','Tangent substitution followed by sine substitution',[
 ('Use tangent and account for all constant factors.',r'x=2\tan\theta,\quad I=\frac14\int\frac{\tan^2\theta}{\sec^3\theta}\,d\theta'),
 ('Rewrite in sine and cosine, then substitute again.',r'I=\frac14\int\sin^2\theta\cos\theta\,d\theta=\frac{\sin^3\theta}{12}+C'),
 ('Use the triangle relation and cube it.',r'\sin\theta=\frac{x}{\sqrt{x^2+4}},\quad I=\frac{x^3}{12(x^2+4)^{3/2}}+C')])
ant(3,9,r'\frac{\sqrt{x^2+1}}x',r'\sqrt{x^2+1}+\ln\left|\frac{x}{1+\sqrt{x^2+1}}\right|','Tangent substitution and a useful split',[
 ('For the positive branch, set tangent equal to x.',r'x=\tan\theta,\quad I=\int\frac{\sec^3\theta}{\tan\theta}\,d\theta'),
 ('Use secant squared equals one plus tangent squared.',r'\frac{\sec^3\theta}{\tan\theta}=\sec\theta\tan\theta+\csc\theta'),
 ('Integrate the two pieces.',r'I=\sec\theta+\ln|\csc\theta-\cot\theta|+C'),
 ('Translate and rationalize the logarithm argument.',r'\sec\theta=\sqrt{x^2+1},\quad \csc\theta-\cot\theta=\frac{\sqrt{x^2+1}-1}{x}=\frac{x}{1+\sqrt{x^2+1}}')], 'Use $x>0$.')
ant(3,10,r'\frac1{x\sqrt{x^2-4}}',r'\frac12\arctan\left(\frac{\sqrt{x^2-4}}2\right)','Watch the negative secant branch',[
 ('Because x is negative, choose a negative secant substitution rather than assuming a positive x.',r'x=-2\sec\theta,\quad 0<\theta<\pi/2,\quad dx=-2\sec\theta\tan\theta\,d\theta'),
 ('The radical is positive; the two other negative signs cancel.',r'\sqrt{x^2-4}=2\tan\theta,\quad I=\int\frac{-2\sec\theta\tan\theta}{-4\sec\theta\tan\theta}\,d\theta=\frac\theta2+C'),
 ('Use inverse tangent to recover the chosen angle without a sign ambiguity.',r'\theta=\arctan\left(\frac{\sqrt{x^2-4}}2\right)')], 'Find an antiderivative on the interval $x<-2$.')

# 5. Partial fractions: distinct factors, repeated factors, and irreducible quadratics.
ant(4,1,r'\frac{3x+5}{(x+1)(x+2)}',r'2\ln|x+1|+\ln|x+2|','Two distinct linear factors',[
 ('Write one constant numerator for each linear factor.',r'\frac{3x+5}{(x+1)(x+2)}=\frac A{x+1}+\frac B{x+2}'),
 ('Clear denominators and substitute the two roots.',r'3x+5=A(x+2)+B(x+1),\quad A=2,\quad B=1'),
 ('Integrate the two reciprocal terms.',r'I=2\ln|x+1|+\ln|x+2|+C')])
ant(4,2,r'\frac{2x+1}{x^2-x-2}',r'\frac53\ln|x-2|+\frac13\ln|x+1|','Factor before decomposing',[
 ('Factor the denominator.',r'x^2-x-2=(x-2)(x+1)'),
 ('Clear denominators and solve for the constants.',r'2x+1=A(x+1)+B(x-2),\quad A=\frac53,\quad B=\frac13'),
 ('Integrate with absolute values on each permitted interval.',r'I=\frac53\ln|x-2|+\frac13\ln|x+1|+C')])
ant(4,3,r'\frac1{x(x+1)^2}',r'\ln|x|-\ln|x+1|+\frac1{x+1}','A repeated linear factor',[
 ('Include both powers of the repeated factor.',r'\frac1{x(x+1)^2}=\frac A{x}+\frac B{x+1}+\frac D{(x+1)^2}'),
 ('Clear denominators, substitute zero and negative one, then compare coefficients.',r'1=A(x+1)^2+Bx(x+1)+Dx,\quad A=1,\quad B=-1,\quad D=-1'),
 ('The last term uses the power rule, not the logarithm rule.',r'I=\ln|x|-\ln|x+1|+\frac1{x+1}+C')])
ant(4,4,r'\frac{x^2+2}{x(x^2+1)}',r'2\ln|x|-\frac12\ln(x^2+1)','A linear and an irreducible quadratic factor',[
 ('Use a linear numerator over the irreducible quadratic.',r'\frac{x^2+2}{x(x^2+1)}=\frac A{x}+\frac{Bx+D}{x^2+1}'),
 ('Equate coefficients after clearing denominators.',r'x^2+2=A(x^2+1)+(Bx+D)x,\quad A=2,\quad B=-1,\quad D=0'),
 ('Use a small substitution for the quadratic term.',r'I=2\int\frac{dx}{x}-\int\frac{x}{x^2+1}\,dx=2\ln|x|-\frac12\ln(x^2+1)+C')])
ant(4,5,r'\frac{x^2}{x^2-1}',r'x+\frac12\ln\left|\frac{x-1}{x+1}\right|','Divide first',[
 ('The fraction is not proper, so do polynomial division first.',r'\frac{x^2}{x^2-1}=1+\frac1{x^2-1}'),
 ('Decompose the remaining proper fraction.',r'\frac1{x^2-1}=\frac12\left(\frac1{x-1}-\frac1{x+1}\right)'),
 ('Integrate and combine logarithms if desired.',r'I=x+\frac12\ln\left|\frac{x-1}{x+1}\right|+C')])
definite(4,6,r'\frac1{(x+1)(x+2)}','0','1',r'\ln(4/3)','Partial fractions with endpoint evaluation',[
 ('Decompose the rational function.',r'\frac1{(x+1)(x+2)}=\frac1{x+1}-\frac1{x+2}'),
 ('Find the logarithmic antiderivative; all arguments here are positive.',r'I=\left[\ln(x+1)-\ln(x+2)\right]_0^1'),
 ('Combine the four endpoint logarithms.',r'I=\ln2-\ln3-\ln1+\ln2=\ln(4/3)')])
ant(4,7,r'\frac{x^2+x+2}{(x+1)(x^2+1)}',r'\ln|x+1|+\arctan x','A quadratic that produces inverse tangent',[
 ('Use the correct numerator degree for each factor.',r'\frac{x^2+x+2}{(x+1)(x^2+1)}=\frac A{x+1}+\frac{Bx+D}{x^2+1}'),
 ('Match coefficients; the linear part of the quadratic numerator vanishes.',r'x^2+x+2=A(x^2+1)+(Bx+D)(x+1),\quad A=1,\quad B=0,\quad D=1'),
 ('Integrate the logarithm and inverse-tangent terms.',r'I=\ln|x+1|+\arctan x+C')])
ant(4,8,r'\frac{x^3+1}{x^2(x-1)}',r'x-\ln|x|+\frac1x+2\ln|x-1|','Division plus a repeated factor',[
 ('First divide, then include every power of the repeated factor.',r'\frac{x^3+1}{x^2(x-1)}=1+\frac{x^2+1}{x^2(x-1)},\quad \frac{x^2+1}{x^2(x-1)}=\frac A{x}+\frac B{x^2}+\frac D{x-1}'),
 ('Clear denominators and compare the constant, linear, and quadratic coefficients.',r'x^2+1=Ax(x-1)+B(x-1)+Dx^2,\quad A=-1,\quad B=-1,\quad D=2'),
 ('Integrate the four resulting terms.',r'I=\int\left(1-\frac1x-\frac1{x^2}+\frac2{x-1}\right)dx'),
 ('Simplify the result, keeping the power-rule sign.',r'I=x-\ln|x|+\frac1x+2\ln|x-1|+C')])
ant(4,9,r'\frac1{(x^2-1)^2}',r'-\frac{x}{2(x^2-1)}+\frac14\ln\left|\frac{x+1}{x-1}\right|','Two repeated linear factors',[
 ('Factor the denominator completely and include four partial-fraction terms.',r'\frac1{(x-1)^2(x+1)^2}=\frac A{x-1}+\frac B{(x-1)^2}+\frac D{x+1}+\frac E{(x+1)^2}'),
 ('Substituting the roots gives the squared-factor coefficients; matching the remaining coefficients gives the others.',r'A=-\frac14,\quad B=\frac14,\quad D=\frac14,\quad E=\frac14'),
 ('Integrate the four terms.',r'I=-\frac14\ln|x-1|-\frac1{4(x-1)}+\frac14\ln|x+1|-\frac1{4(x+1)}+C'),
 ('Combine the rational terms and the logarithms.',r'I=-\frac{x}{2(x^2-1)}+\frac14\ln\left|\frac{x+1}{x-1}\right|+C')])
ant(4,10,r'\frac{x^2-1}{x^3-x}',r'\ln|x|','Cancel factors but keep the original domain',[
 ('Factor before setting up unnecessary partial fractions.',r'\frac{x^2-1}{x^3-x}=\frac{(x-1)(x+1)}{x(x-1)(x+1)}=\frac1x'),
 ('Cancellation simplifies the formula, but does not make the original expression defined at the canceled roots.',r'x\ne-1,\quad x\ne0,\quad x\ne1'),
 ('Integrate on each interval of the original domain; constants may differ between intervals.',r'I=\ln|x|+C')])

# 6. Mixed review: choose the method without a topic-specific hint.
ant(5,1,r'x^3e^{x^2}',r'\frac12e^{x^2}(x^2-1)','Substitution followed by parts',[
 ('Use the exponent as the new variable and rewrite the leftover square.',r'u=x^2,\quad du=2x\,dx,\quad I=\frac12\int ue^u\,du'),
 ('Apply integration by parts in the new variable.',r'\int ue^u\,du=ue^u-e^u'),
 ('Substitute back and factor.',r'I=\frac12e^{x^2}(x^2-1)+C')])
ant(5,2,r'\frac{\ln x}{x(1+\ln x)}',r'\ln x-\ln|1+\ln x|','Substitution and rational simplification',[
 ('Use the logarithm as the new variable.',r'u=\ln x,\quad du=\frac{dx}{x},\quad I=\int\frac{u}{1+u}\,du'),
 ('Divide the numerator by the denominator.',r'\frac{u}{1+u}=1-\frac1{1+u}'),
 ('Integrate and restore the logarithm.',r'I=\ln x-\ln|1+\ln x|+C')], 'Work on intervals where $x>0$ and $x\ne e^{-1}$.')
ant(5,3,r'x\arctan(x^2)',r'\frac{x^2}{2}\arctan(x^2)-\frac14\ln(1+x^4)','Substitution and inverse-tangent parts',[
 ('First remove the repeated square.',r'u=x^2,\quad I=\frac12\int\arctan u\,du'),
 ('Use integration by parts on the inverse tangent.',r'I=\frac12\left(u\arctan u-\int\frac{u}{1+u^2}\,du\right)'),
 ('The last integral is logarithmic; substitute back.',r'I=\frac{x^2}{2}\arctan(x^2)-\frac14\ln(1+x^4)+C')])
ant(5,4,r'\frac{x^2}{x^2+4}',r'x-2\arctan(x/2)','Division and an inverse-tangent form',[
 ('Separate the fraction into a constant and a simpler reciprocal.',r'\frac{x^2}{x^2+4}=1-\frac4{x^2+4}'),
 ('Scale the quadratic reciprocal to the inverse-tangent form.',r'\int\frac{dx}{x^2+4}=\frac12\arctan(x/2)'),
 ('Combine the antiderivatives.',r'I=x-2\arctan(x/2)+C')])
ant(5,5,r'\frac{1+\tan^2x}{3+\tan x}',r'\ln|3+\tan x|','Recognize a derivative through an identity',[
 ('Rewrite the numerator.',r'1+\tan^2x=\sec^2x'),
 ('Substitute the denominator.',r'u=3+\tan x,\quad du=\sec^2x\,dx,\quad I=\int\frac{du}{u}'),
 ('Use the logarithm rule on intervals where the original integrand exists.',r'I=\ln|3+\tan x|+C')])
ant(5,6,r'\sin x\ln(2+\cos x)',r'-(2+\cos x)\ln(2+\cos x)+(2+\cos x)','Substitution followed by logarithmic parts',[
 ('Substitute inside the logarithm and keep its derivative sign.',r'u=2+\cos x,\quad du=-\sin x\,dx,\quad I=-\int\ln u\,du'),
 ('Integrate the logarithm by parts.',r'\int\ln u\,du=u\ln u-u'),
 ('Distribute the minus sign and substitute back.',r'I=-(2+\cos x)\ln(2+\cos x)+(2+\cos x)+C')])
ant(5,7,r'\frac{e^x}{e^{2x}+3e^x+2}',r'\ln\left(\frac{e^x+1}{e^x+2}\right)','Exponential substitution and partial fractions',[
 ('Turn the exponentials into a rational integral.',r'u=e^x,\quad du=e^x\,dx,\quad I=\int\frac{du}{(u+1)(u+2)}'),
 ('Decompose the reciprocal product.',r'\frac1{(u+1)(u+2)}=\frac1{u+1}-\frac1{u+2}'),
 ('Integrate and combine the logarithms; both arguments are positive.',r'I=\ln\left(\frac{e^x+1}{e^x+2}\right)+C')])
ant(5,8,r'\frac{\ln(1+x^2)}{x^3}',r'-\frac{\ln(1+x^2)}{2x^2}+\ln|x|-\frac12\ln(1+x^2)','Parts followed by partial fractions',[
 ('Differentiate the logarithm and integrate the reciprocal cube.',r'u=\ln(1+x^2),\quad dv=x^{-3}\,dx,\quad v=-\frac1{2x^2}'),
 ('Apply parts and simplify the remaining integrand.',r'I=-\frac{\ln(1+x^2)}{2x^2}+\int\frac{dx}{x(1+x^2)}'),
 ('Decompose the rational term.',r'\frac1{x(1+x^2)}=\frac1x-\frac{x}{1+x^2}'),
 ('Integrate both terms.',r'I=-\frac{\ln(1+x^2)}{2x^2}+\ln|x|-\frac12\ln(1+x^2)+C')])
ant(5,9,r'x^3\ln(1+x^2)',r'\frac{x^4-1}{4}\ln(1+x^2)-\frac{x^4}{8}+\frac{x^2}{4}','Substitution then two parts calculations',[
 ('Replace the quadratic and the leftover square.',r'u=1+x^2,\quad x^3\,dx=\frac12(u-1)\,du'),
 ('Split the integral into two logarithmic products.',r'I=\frac12\int u\ln u\,du-\frac12\int\ln u\,du'),
 ('Apply parts to each term.',r'I=\left(\frac{u^2}{4}-\frac u2\right)\ln u-\frac{u^2}{8}+\frac u2+C'),
 ('Expand after substituting back. Absorb the resulting constant into C.',r'I=\frac{x^4-1}{4}\ln(1+x^2)-\frac{x^4}{8}+\frac{x^2}{4}+C')])
definite(5,10,r'x\cos^2x',r'-\pi/2',r'\pi/2','0','Choose symmetry instead of unnecessary parts',[
 ('Check the parity before expanding the square.',r'\cos^2(-x)=\cos^2x,\quad f(-x)=-f(x)'),
 ('The integrand is continuous and odd on symmetric limits.',r'\int_{-a}^{a}f(x)\,dx=0'),
 ('Apply the rule with the given bound.',r'a=\pi/2,\quad I=0')])

# 7. Improper integrals: both infinite endpoints and finite singularities.
definite(6,1,r'\frac1{x^{3/2}}','1',r'\infty','2','Infinite-endpoint limit',[
 ('Replace infinity with a finite endpoint.',r'I=\lim_{b\to\infty}\int_1^b x^{-3/2}\,dx'),
 ('Integrate before taking the limit.',r'I=\lim_{b\to\infty}\left[-2x^{-1/2}\right]_1^b=\lim_{b\to\infty}\left(2-\frac2{\sqrt b}\right)'),
 ('The limit is finite, so the improper integral converges.',r'I=2')],True)
definite(6,2,r'\ln x','0','1','-1','Logarithmic endpoint singularity',[
 ('The logarithm is unbounded at zero. Approach that endpoint from the right.',r'I=\lim_{a\to0^+}\int_a^1\ln x\,dx'),
 ('Use integration by parts.',r'I=\lim_{a\to0^+}\left[x\ln x-x\right]_a^1=\lim_{a\to0^+}(-1-a\ln a+a)'),
 ('The product tends to zero, despite the logarithm itself diverging.',r'\lim_{a\to0^+}a\ln a=0,\quad I=-1\quad\text{(convergent)}')],True)
definite(6,3,r'\frac1{\sqrt{4-x}}','0','4','4','A singular upper endpoint',[
 ('The denominator vanishes at the upper endpoint, so use a one-sided limit.',r'I=\lim_{b\to4^-}\int_0^b(4-x)^{-1/2}\,dx'),
 ('Substitute the radicand or use its chain-rule factor.',r'I=\lim_{b\to4^-}\left[-2\sqrt{4-x}\right]_0^b'),
 ('Evaluate the finite limit.',r'I=\lim_{b\to4^-}(4-2\sqrt{4-b})=4')],True)
definite(6,4,r'\frac1{x(x+1)}','1',r'\infty',r'\ln2','Partial fractions before the infinite limit',[
 ('Decompose the integrand.',r'\frac1{x(x+1)}=\frac1x-\frac1{x+1}'),
 ('Keep the logarithms combined before taking the limit.',r'I=\lim_{b\to\infty}\left[\ln\frac{x}{x+1}\right]_1^b'),
 ('The upper ratio tends to one. Do not treat the two divergent logarithms separately.',r'I=\ln1-\ln(1/2)=\ln2')],True)
definite(6,5,r'e^{-2x}','0',r'\infty',r'\frac12','Exponential decay',[
 ('Replace the infinite endpoint by a limit.',r'I=\lim_{b\to\infty}\int_0^b e^{-2x}\,dx'),
 ('Integrate and evaluate both endpoints.',r'I=\lim_{b\to\infty}\left[-\frac12e^{-2x}\right]_0^b'),
 ('Exponential decay makes the limit finite.',r'I=\lim_{b\to\infty}\frac{1-e^{-2b}}2=\frac12')],True)
definite(6,6,r'\frac1{x\ln x}','e',r'\infty',r'\text{Diverges to }+\infty','A borderline logarithmic divergence',[
 ('Use a logarithmic substitution and transform the lower endpoint.',r'u=\ln x,\quad du=\frac{dx}{x},\quad x=e\Rightarrow u=1'),
 ('The integral becomes the divergent reciprocal integral.',r'I=\lim_{B\to\infty}\int_1^B\frac{du}{u}=\lim_{B\to\infty}\ln B'),
 ('A denominator growing slightly faster than x does not guarantee convergence.',r'I=+\infty\quad\text{so the integral diverges}')],True)
PROBLEMS[-1]['check']['expected'] = 'oo'
definite(6,7,r'\frac1{x^{2/3}}','0','1','3','An integrable power singularity',[
 ('Approach zero from the right.',r'I=\lim_{a\to0^+}\int_a^1x^{-2/3}\,dx'),
 ('The power rule gives a positive one-third power.',r'I=\lim_{a\to0^+}\left[3x^{1/3}\right]_a^1'),
 ('The antiderivative has a finite limit at zero, so the integral converges.',r'I=\lim_{a\to0^+}3(1-a^{1/3})=3')],True)
definite(6,8,r'\frac{x}{(1+x^2)^2}','0',r'\infty',r'\frac12','Substitution with an infinite bound',[
 ('Replace the upper endpoint temporarily, then substitute.',r'u=1+x^2,\quad du=2x\,dx,\quad I=\lim_{b\to\infty}\frac12\int_1^{1+b^2}u^{-2}\,du'),
 ('Integrate the negative power.',r'I=\lim_{b\to\infty}\left[-\frac1{2u}\right]_1^{1+b^2}'),
 ('The upper contribution vanishes.',r'I=\lim_{b\to\infty}\left(\frac12-\frac1{2(1+b^2)}\right)=\frac12')],True)
definite(6,9,r'\frac{x^2}{(1+x^2)^2}','0',r'\infty',r'\frac\pi4','Trigonometric substitution for an improper integral',[
 ('Choose tangent; the infinite endpoint becomes a one-sided angle limit.',r'x=\tan\theta,\quad dx=\sec^2\theta\,d\theta,\quad x\to\infty\Rightarrow\theta\to\pi/2^-'),
 ('Simplify the powers completely.',r'\frac{\tan^2\theta\sec^2\theta}{\sec^4\theta}=\sin^2\theta'),
 ('Reduce the square and evaluate the limit.',r'I=\lim_{t\to\pi/2^-}\left[\frac\theta2-\frac{\sin2\theta}{4}\right]_0^t=\frac\pi4')],True)
add(6,10,'Determine whether this improper integral converges. Explain why symmetric cancellation is or is not valid.',r'\int_{-1}^1\frac{dx}{x}',r'\text{Diverges (the two one-sided integrals do not converge)}','Split at the interior singularity',[
 ('The integrand is undefined inside the interval. Each side must converge independently.',r'I=\int_{-1}^0\frac{dx}{x}+\int_0^1\frac{dx}{x}'),
 ('Evaluate the two limits separately.',r'\lim_{b\to0^-}[\ln|x|]_{-1}^{b}=-\infty,\qquad \lim_{a\to0^+}[\ln x]_{a}^{1}=+\infty'),
 ('Opposite infinities cannot be canceled. Symmetric cutoffs give a principal value of zero, which is not convergence of the improper integral.',r'\text{The ordinary improper integral diverges.}')],
 dict(kind='divergence',pieces=[dict(integrand='1/x',lower='-1',upper='0',expected='-oo'),dict(integrand='1/x',lower='0',upper='1',expected='oo')]))

# 8. Areas: establish intersections and the correct nonnegative height first.
geometry(7,1,'Find the total area enclosed by these curves.',r'y=2x,\qquad y=x^2',r'\frac43','Top minus bottom',[
 ('Solve for the intersection points.',r'x^2=2x\Rightarrow x=0,2'),
 ('The line is above the parabola between the intersections.',r'A=\int_0^2(2x-x^2)\,dx'),
 ('Integrate and evaluate.',r'A=\left[x^2-\frac{x^3}{3}\right]_0^2=\frac43')],[(r'2x-x^2','0','2')])
geometry(7,2,'Find the total area enclosed by these curves.',r'y=\sqrt x,\qquad y=\frac x2',r'\frac43','Check intersections after squaring',[
 ('Solve the equation on the shared domain and check both candidates.',r'\sqrt x=x/2,\quad x\ge0\Rightarrow x=0,4'),
 ('The square-root curve is above the line on this interval.',r'A=\int_0^4\left(\sqrt x-\frac x2\right)dx'),
 ('Evaluate the area integral.',r'A=\left[\frac23x^{3/2}-\frac{x^2}{4}\right]_0^4=\frac{16}{3}-4=\frac43')],[(r'\sqrt x-x/2','0','4')])
geometry(7,3,'Find the total area enclosed by the parabola and line.',r'y=x^2,\qquad y=x+2',r'\frac92','Intersections on both sides of zero',[
 ('Find the bounds by equating the curves.',r'x^2=x+2\Rightarrow(x-2)(x+1)=0\Rightarrow x=-1,2'),
 ('The line is the upper boundary throughout the interval.',r'A=\int_{-1}^2(x+2-x^2)\,dx'),
 ('Evaluate both endpoints, including the negative lower bound.',r'A=\left[\frac{x^2}{2}+2x-\frac{x^3}{3}\right]_{-1}^2=\frac92')],[(r'x+2-x^2','-1','2')])
geometry(7,4,'Find the total area of all bounded regions between the two curves.',r'y=x,\qquad y=x^3',r'\frac12','Split where the upper curve changes',[
 ('There are three intersections, so there are two bounded regions.',r'x=x^3\Rightarrow x=-1,0,1'),
 ('Use the cubic above the line on the negative interval, and the line above the cubic on the positive interval.',r'A=\int_{-1}^0(x^3-x)\,dx+\int_0^1(x-x^3)\,dx'),
 ('Symmetry gives equal positive areas.',r'A=2\left[\frac{x^2}{2}-\frac{x^4}{4}\right]_0^1=\frac12')],[(r'x^3-x','-1','0'),(r'x-x^3','0','1')])
geometry(7,5,'Find the area between the curves on the stated interval.',r'y=\sin x,\quad y=\cos x,\quad 0\le x\le\pi/2',r'2\sqrt2-2','Split at a trigonometric intersection',[
 ('Find where the curves exchange order.',r'\sin x=\cos x\Rightarrow x=\pi/4'),
 ('Cosine is higher first; sine is higher afterward.',r'A=\int_0^{\pi/4}(\cos x-\sin x)\,dx+\int_{\pi/4}^{\pi/2}(\sin x-\cos x)\,dx'),
 ('Evaluate the two equal areas.',r'A=(\sqrt2-1)+(\sqrt2-1)=2\sqrt2-2')],[(r'\cos x-\sin x','0',r'\pi/4'),(r'\sin x-\cos x',r'\pi/4',r'\pi/2')])
geometry(7,6,'Find the enclosed area using horizontal slices.',r'x=y^2,\qquad x=2y',r'\frac43','Right minus left with respect to y',[
 ('Equate the horizontal coordinates to find the vertical bounds.',r'y^2=2y\Rightarrow y=0,2'),
 ('The line is the right boundary and the parabola is the left boundary.',r'A=\int_0^2(2y-y^2)\,dy'),
 ('Evaluate in y.',r'A=\left[y^2-\frac{y^3}{3}\right]_0^2=\frac43')],[(r'2y-y^2','0','2')],variable='y')
geometry(7,7,'Find the area bounded by the logarithmic curve, the x-axis, and the two vertical lines.',r'y=\ln x,\quad y=0,\quad x=1,\quad x=e','1','Area requiring integration by parts',[
 ('The logarithm is nonnegative on the entire interval.',r'A=\int_1^e\ln x\,dx'),
 ('Use integration by parts for the antiderivative.',r'\int\ln x\,dx=x\ln x-x'),
 ('The upper value is zero, but the lower value is negative.',r'A=[x\ln x-x]_1^e=0-(-1)=1')],[(r'\ln x','1','e')])
geometry(7,8,'Find the total area between the curve and the x-axis over this interval.',r'y=x^3-x,\quad -2\le x\le2','5','Four sign intervals',[
 ('Find every zero inside the interval, not just the endpoints.',r'x^3-x=x(x-1)(x+1)=0\Rightarrow x=-1,0,1'),
 ('Use odd symmetry of the function to double the positive-side area; the function changes sign at one.',r'A=2\left(\int_0^1(x-x^3)\,dx+\int_1^2(x^3-x)\,dx\right)'),
 ('Evaluate the inner and outer lobes separately.',r'\int_0^1(x-x^3)\,dx=\frac14,\quad \int_1^2(x^3-x)\,dx=\frac94'),
 ('Add positive areas rather than signed integrals.',r'A=2\left(\frac14+\frac94\right)=5')],[(r'2(x-x^3)','0','1'),(r'2(x^3-x)','1','2')])
geometry(7,9,'Find the total area enclosed by the absolute-value graph and the parabola.',r'y=|x|,\qquad y=x^2-2',r'\frac{20}{3}','Split the absolute value and exploit symmetry',[
 ('On the positive side, solve the intersection equation, then reflect the valid solution.',r'x=x^2-2,\quad x\ge0\Rightarrow x=2;\quad \text{other intersection: }x=-2'),
 ('The absolute-value graph is above the parabola between the intersections.',r'A=2\int_0^2\left(x-(x^2-2)\right)dx'),
 ('Integrate the polynomial height.',r'A=2\left[\frac{x^2}{2}-\frac{x^3}{3}+2x\right]_0^2=\frac{20}{3}')],[(r'2(x-x^2+2)','0','2')])
geometry(7,10,'Find the geometric area between the curve and the x-axis, restricted by the two vertical lines.',r'y=x^2-4,\quad y=0,\quad x=-1,\quad x=1',r'\frac{22}{3}','Area is positive even below the axis',[
 ('The curve lies below the x-axis on the entire interval.',r'x^2-4<0\quad\text{for }-1\le x\le1'),
 ('Subtract the lower curve from the upper boundary zero.',r'A=\int_{-1}^1\left(0-(x^2-4)\right)dx'),
 ('The signed integral of the curve would be negative; this area is positive.',r'A=\left[4x-\frac{x^3}{3}\right]_{-1}^1=\frac{22}{3}')],[(r'4-x^2','-1','1')])

# 9. Volumes by slicing: disks, washers, and prescribed cross sections.
geometry(8,1,'Rotate the bounded region about the x-axis. Find its volume using disks.',r'y=x^2,\quad y=0,\quad x=0,\quad x=2',r'\frac{32\pi}{5}','Square the disk radius',[
 ('A vertical slice sweeps out a disk whose radius is the height of the curve.',r'R(x)=x^2,\quad A(x)=\pi R(x)^2=\pi x^4'),
 ('Integrate the cross-sectional area over the horizontal bounds.',r'V=\pi\int_0^2x^4\,dx'),
 ('Evaluate and report cubic units.',r'V=\pi\left[\frac{x^5}{5}\right]_0^2=\frac{32\pi}{5}')],[(r'\pi x^4','0','2')])
geometry(8,2,'Rotate the region between the curves about the x-axis. Find the volume using washers.',r'y=x,\qquad y=x^2',r'\frac{2\pi}{15}','Outer radius squared minus inner radius squared',[
 ('The intersections are zero and one; the line is higher between them.',r'R=x,\quad r=x^2,\quad 0\le x\le1'),
 ('Subtract squared radii, not the square of their difference.',r'V=\pi\int_0^1(R^2-r^2)\,dx=\pi\int_0^1(x^2-x^4)\,dx'),
 ('Evaluate the polynomial integral.',r'V=\pi\left(\frac13-\frac15\right)=\frac{2\pi}{15}')],[(r'\pi(x^2-x^4)','0','1')])
geometry(8,3,'Rotate the region under the curve and above the x-axis, on the stated interval, about the line y = -1. Use washers.',r'y=\sqrt x,\quad 0\le x\le4',r'\frac{56\pi}{3}','Measure radii from the shifted axis',[
 ('Measure both distances from the horizontal axis of rotation.',r'R=\sqrt x+1,\quad r=1'),
 ('Expand the difference of squares.',r'V=\pi\int_0^4\left((\sqrt x+1)^2-1\right)dx=\pi\int_0^4(x+2\sqrt x)\,dx'),
 ('Evaluate the volume.',r'V=\pi\left[\frac{x^2}{2}+\frac43x^{3/2}\right]_0^4=\frac{56\pi}{3}')],[(r'\pi(x+2\sqrt x)','0','4')])
geometry(8,4,'A solid has this region as its base. Cross sections perpendicular to the x-axis are squares whose sides lie in the base. Find the volume.',r'y=x^2,\qquad y=4',r'\frac{512}{15}','Square cross sections',[
 ('The base extends between the intersections of the parabola and horizontal line.',r'x=-2,2,\quad s(x)=4-x^2'),
 ('Each cross-sectional area is the square of the full vertical side length.',r'A(x)=(4-x^2)^2,\quad V=\int_{-2}^2(4-x^2)^2\,dx'),
 ('Expand and use symmetry.',r'V=2\int_0^2(16-8x^2+x^4)\,dx=\frac{512}{15}')],[(r'(4-x^2)^2','-2','2')])
geometry(8,5,'A solid has the circular disk as its base. Cross sections perpendicular to the x-axis are semicircles whose diameters lie across the base. Find the volume.',r'x^2+y^2\le9',r'18\pi','A semicircle uses half the diameter as its radius',[
 ('A vertical chord gives the diameter, not the radius.',r'd(x)=2\sqrt{9-x^2},\quad r(x)=\sqrt{9-x^2}'),
 ('Use half the area of a full circle.',r'A(x)=\frac\pi2(9-x^2),\quad -3\le x\le3'),
 ('Integrate the cross-sectional area.',r'V=\frac\pi2\int_{-3}^3(9-x^2)\,dx=18\pi')],[(r'\frac\pi2(9-x^2)','-3','3')])
geometry(8,6,'Rotate the region bounded by the line and parabola about the x-axis. Find its volume.',r'y=2x,\qquad y=x^2',r'\frac{64\pi}{15}','Washers between two curves',[
 ('Find the intersections and identify the outer curve.',r'x^2=2x\Rightarrow x=0,2;\quad R=2x,\quad r=x^2'),
 ('Set up the washer integral.',r'V=\pi\int_0^2\left((2x)^2-(x^2)^2\right)dx'),
 ('Evaluate the two power terms.',r'V=\pi\left[\frac{4x^3}{3}-\frac{x^5}{5}\right]_0^2=\frac{64\pi}{15}')],[(r'\pi(4x^2-x^4)','0','2')])
geometry(8,7,'The base lies under the square-root curve and above the x-axis on the stated interval. Perpendicular to the x-axis, the cross sections are equilateral triangles with one side in the base. Find the volume.',r'y=\sqrt x,\quad 0\le x\le1',r'\frac{\sqrt3}{8}','Equilateral-triangle cross sections',[
 ('The triangle side is the vertical distance across the base.',r's(x)=\sqrt x'),
 ('Use the equilateral-triangle area formula.',r'A(x)=\frac{\sqrt3}{4}s(x)^2=\frac{\sqrt3}{4}x'),
 ('Integrate over the base interval.',r'V=\frac{\sqrt3}{4}\int_0^1x\,dx=\frac{\sqrt3}{8}')],[(r'\frac{\sqrt3}{4}x','0','1')])
geometry(8,8,'Rotate the entire region between the parabola and horizontal line about y = 5. Find the volume using washers.',r'y=x^2,\qquad y=4',r'\frac{832\pi}{15}','An axis above both curves',[
 ('The region spans negative two to two. The lower curve is farther from the axis above it.',r'R=5-x^2,\quad r=5-4=1'),
 ('Set up the correct difference of squared distances.',r'V=\pi\int_{-2}^2\left((5-x^2)^2-1\right)dx'),
 ('Expand and use the even symmetry.',r'V=2\pi\int_0^2(24-10x^2+x^4)\,dx'),
 ('Evaluate the three power terms.',r'V=2\pi\left[24x-\frac{10x^3}{3}+\frac{x^5}{5}\right]_0^2=\frac{832\pi}{15}')],[(r'\pi(24-10x^2+x^4)','-2','2')])
geometry(8,9,'Rotate the region between the curves about the vertical line x = -1. Use horizontal washers, not shells.',r'y=x^2,\qquad y=2x',r'\frac{16\pi}{3}','Solve for x before using horizontal washers',[
 ('The region is in the first quadrant, with y from zero to four. Solve each boundary for x.',r'x_{\rm left}=y/2,\quad x_{\rm right}=\sqrt y'),
 ('Measure the outer and inner radii from the vertical axis.',r'R=\sqrt y+1,\quad r=y/2+1'),
 ('Subtract squares and simplify in y.',r'V=\pi\int_0^4\left((\sqrt y+1)^2-(y/2+1)^2\right)dy=\pi\int_0^4\left(2\sqrt y-\frac{y^2}{4}\right)dy'),
 ('Evaluate the two powers.',r'V=\pi\left[\frac43y^{3/2}-\frac{y^3}{12}\right]_0^4=\frac{16\pi}{3}')],[(r'\pi(2\sqrt y-y^2/4)','0','4')],variable='y')
geometry(8,10,'Rotate the region under the line and above the x-axis, from x = 0 to x = 2, about y = 1. Find the volume. The axis passes through the region.',r'y=x+1,\quad y=0,\quad 0\le x\le2',r'\frac{10\pi}{3}','An axis through the region produces disks',[
 ('Every vertical segment crosses the rotation axis. There is no inner hole; choose the farther endpoint as the disk radius.',r'R(x)=\max(1,x)'),
 ('The farthest endpoint changes when the two distances are equal.',r'R=1\text{ on }[0,1],\quad R=x\text{ on }[1,2]'),
 ('Split the disk integral at that point.',r'V=\pi\int_0^1 1\,dx+\pi\int_1^2x^2\,dx'),
 ('Evaluate. Subtracting the squared distances would incorrectly remove part of the solid.',r'V=\pi\left(1+\frac{8-1}{3}\right)=\frac{10\pi}{3}')],[(r'\pi','0','1'),(r'\pi x^2','1','2')])

# 10. Cylindrical shells: choose radius and height in the correct variable.
geometry(9,1,'Use cylindrical shells to find the volume when this region is rotated about the y-axis.',r'0\le y\le x^2,\quad 0\le x\le2',r'8\pi','Vertical shells',[
 ('A vertical strip is parallel to the y-axis.',r'r=x,\quad h=x^2'),
 ('Multiply circumference, height, and thickness.',r'V=2\pi\int_0^2x\cdot x^2\,dx'),
 ('Evaluate the power integral.',r'V=2\pi\left[\frac{x^4}{4}\right]_0^2=8\pi')],[(r'2\pi x^3','0','2')])
geometry(9,2,'Use shells to rotate the first-quadrant region under the parabola about the y-axis.',r'y=4-x^2,\quad y=0,\quad x\ge0',r'8\pi','Shells under a parabola',[
 ('Find where the parabola reaches the x-axis in the first quadrant.',r'4-x^2=0\Rightarrow x=2'),
 ('The radius is x and the height is the parabola height.',r'V=2\pi\int_0^2x(4-x^2)\,dx'),
 ('Integrate and evaluate.',r'V=2\pi\left[2x^2-\frac{x^4}{4}\right]_0^2=8\pi')],[(r'2\pi x(4-x^2)','0','2')])
geometry(9,3,'Use shells to rotate the region between the curves about the y-axis.',r'y=x,\qquad y=x^2',r'\frac\pi6','Shell height is a difference of curves',[
 ('The two intersections are zero and one.',r'x=x^2\Rightarrow x=0,1'),
 ('Use the line minus the parabola for the height.',r'r=x,\quad h=x-x^2,\quad V=2\pi\int_0^1x(x-x^2)\,dx'),
 ('Evaluate the two powers.',r'V=2\pi\left(\frac13-\frac14\right)=\frac\pi6')],[(r'2\pi x(x-x^2)','0','1')])
geometry(9,4,'Rotate the region under the logarithm and above the x-axis, between x = 1 and x = e, about the y-axis. Use shells.',r'y=\ln x,\quad 1\le x\le e',r'\frac\pi2(e^2+1)','Shells requiring integration by parts',[
 ('Use x for the radius and the logarithm for the height.',r'V=2\pi\int_1^e x\ln x\,dx'),
 ('Integrate by parts.',r'\int x\ln x\,dx=\frac{x^2}{2}\ln x-\frac{x^2}{4}'),
 ('Evaluate upper minus lower before multiplying by two pi.',r'V=2\pi\left(\frac{e^2}{4}+\frac14\right)=\frac\pi2(e^2+1)')],[(r'2\pi x\ln x','1','e')])
geometry(9,5,'Rotate the region under the square-root curve and above the x-axis, from x = 0 to x = 4, about x = -1. Use shells.',r'y=\sqrt x,\quad 0\le x\le4',r'\frac{544\pi}{15}','Shells around a shifted vertical axis',[
 ('The radius is the distance from the strip to the line x = -1.',r'r=x+1,\quad h=\sqrt x'),
 ('Expand the product into two powers.',r'V=2\pi\int_0^4(x+1)\sqrt x\,dx=2\pi\int_0^4(x^{3/2}+x^{1/2})\,dx'),
 ('Evaluate both antiderivatives.',r'V=2\pi\left[\frac25x^{5/2}+\frac23x^{3/2}\right]_0^4=\frac{544\pi}{15}')],[(r'2\pi(x+1)\sqrt x','0','4')])
geometry(9,6,'Use horizontal shells to rotate the region between the curves about the x-axis.',r'x=y^2,\qquad x=2y',r'\frac{8\pi}{3}','Horizontal shells use dy',[
 ('Find the vertical bounds and identify the right boundary.',r'y^2=2y\Rightarrow y=0,2,\quad x_{\rm right}=2y'),
 ('The radius is y, and shell height is the horizontal width.',r'r=y,\quad h=2y-y^2,\quad V=2\pi\int_0^2y(2y-y^2)\,dy'),
 ('Integrate with respect to y.',r'V=2\pi\left[\frac{2y^3}{3}-\frac{y^4}{4}\right]_0^2=\frac{8\pi}{3}')],[(r'2\pi y(2y-y^2)','0','2')],variable='y')
geometry(9,7,'Rotate the region under the exponential curve and above the x-axis on the stated interval about the y-axis. Use shells.',r'y=e^{-x},\quad 0\le x\le1',r'2\pi\left(1-\frac2e\right)','Shells and exponential integration by parts',[
 ('Write radius times height.',r'V=2\pi\int_0^1xe^{-x}\,dx'),
 ('Differentiate x and integrate the exponential.',r'\int xe^{-x}\,dx=-(x+1)e^{-x}'),
 ('Evaluate both endpoints.',r'V=2\pi\left[-(x+1)e^{-x}\right]_0^1=2\pi\left(1-\frac2e\right)')],[(r'2\pi xe^{-x}','0','1')])
geometry(9,8,'Rotate the region between the curves about the line x = 3. Use cylindrical shells.',r'y=x^2,\qquad y=2x',r'\frac{16\pi}{3}','An axis to the right of the region',[
 ('The region extends from zero to two, entirely to the left of the rotation axis.',r'r=3-x,\quad h=2x-x^2'),
 ('Use a positive distance for the radius.',r'V=2\pi\int_0^2(3-x)(2x-x^2)\,dx'),
 ('Expand before integrating.',r'(3-x)(2x-x^2)=6x-5x^2+x^3'),
 ('Evaluate the resulting polynomial.',r'V=2\pi\left[3x^2-\frac{5x^3}{3}+\frac{x^4}{4}\right]_0^2=\frac{16\pi}{3}')],[(r'2\pi(3-x)(2x-x^2)','0','2')])
geometry(9,9,'Rotate the entire region between the sideways parabola and vertical line about y = -3. Use horizontal shells.',r'x=y^2,\qquad x=4',r'64\pi','Shifted horizontal axis and symmetry',[
 ('The vertical bounds come from the intersections.',r'y^2=4\Rightarrow y=-2,2'),
 ('Measure the radius from the line below the region; the height is the horizontal width.',r'r=y+3,\quad h=4-y^2,\quad V=2\pi\int_{-2}^2(y+3)(4-y^2)\,dy'),
 ('Only the odd part cancels. The radius itself is not an even function.',r'(y+3)(4-y^2)=4y-y^3+12-3y^2'),
 ('Integrate the even part.',r'V=2\pi\int_{-2}^2(12-3y^2)\,dy=64\pi')],[(r'2\pi(y+3)(4-y^2)','-2','2')],variable='y')
geometry(9,10,'Rotate the entire symmetric region under the parabola and above the x-axis about the y-axis. Use shells without counting the same volume twice.',r'y=4-x^2,\quad y=0,\quad -2\le x\le2',r'8\pi','Symmetric strips can sweep the same shell',[
 ('Strips at opposite x-values produce the same shell, because they have equal radius and height.',r'r=|x|,\quad h=4-x^2'),
 ('Use just the right half of the region; it already sweeps out the complete solid.',r'V=2\pi\int_0^2x(4-x^2)\,dx'),
 ('Evaluate once. Integrating the positive shell formula over both halves would double-count the solid.',r'V=2\pi\left[2x^2-\frac{x^4}{4}\right]_0^2=8\pi')],[(r'2\pi x(4-x^2)','0','2')])

assert len(PROBLEMS) == 100
assert [p['id'] for p in PROBLEMS] == [f'ans{i}' for i in range(1,101)]
