from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/guide', methods=['GET', 'POST'])
def guide():
    if request.method == 'POST':
        cargotype = request.form.get('cargo_type')          
        modetransport = request.form.get('transport_mode')   
        regionto = request.form.get('region')             
        user = request.form.get('role')                
        responsible = request.form.get('responsibility_level') 
        insured = request.form.get('insurance')             
        impoclear = request.form.get('import_clearance')     
        deliveryp = request.form.get('delivery_point')    
        experience = request.form.get('experience_level')   
        incotermResult = None

        # easier for domestic
        if regionto == 'domestic':
            if user == 'seller' and responsible == 'minimal':
                incotermResult = 'EXW'
            elif deliveryp == 'destination_premises':
                incotermResult = 'DAP'
            elif responsible == 'maximal':
                incotermResult = 'DDP'

        else:
            # international shipments
            if user == 'seller':
                if responsible == 'minimal':
                    incotermResult = 'EXW'
                elif responsible == 'shared':
                    incotermResult = 'FAS' if modetransport == 'sea' else 'FCA'
                elif responsible == 'maximal':
                    if deliveryp in ['port_of_arrival', 'destination_premises'] and modetransport in ['sea', 'road', 'rail']:
                        incotermResult = 'DPU'
                    elif insured == 'yes':
                        incotermResult = 'CIF' if modetransport == 'sea' else 'CIP'
                    else:
                        incotermResult = 'CFR' if modetransport == 'sea' else 'CPT'
            elif user == 'buyer':
                if responsible == 'minimal':
                    incotermResult = 'DAP' if impoclear == 'buyer' else 'DDP'
                elif responsible == 'shared':
                    if modetransport == 'sea' and deliveryp == 'port_of_shipment':
                        incotermResult = 'FOB'
                    else:
                        incotermResult = 'FCA'
                elif responsible == 'maximal':
                    incotermResult = 'EXW' if deliveryp == 'origin_premises' else 'FCA'

        # beginners are more safe
        if experience == 'beginner':
            if incotermResult in ['FCA', 'FOB', 'CFR', 'CIF', 'FAS']:
                incotermResult = 'DAP'

        if cargotype == 'project' and responsible == 'maximal':
            incotermResult = 'DPU'
        elif cargotype == 'breakbulk' and modetransport == 'sea' and user == 'seller':
            incotermResult = 'FAS'

        #result dictionary
        results = {
            'cargo_type': cargotype,
            'transport_mode': modetransport,
            'region': regionto,
            'role': user,
            'responsibility_level': responsible,
            'insurance': insured,
            'import_clearance': impoclear,
            'delivery_point': deliveryp,
            'experience_level': experience,
            'recommendation': incotermResult
        }

        return render_template('guide.html', result=results)

    return render_template('guide.html')

@app.route('/incoterm/<term>')
def incoterm(term):
    return render_template(f"incoterms/{term.upper()}.html") #help from ChatGPT direct the user to the specific incoterm

if __name__ == '__main__':
    app.run(debug=True)





