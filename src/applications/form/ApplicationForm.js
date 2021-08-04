import React, {useState,useEffect} from 'react'
import { Grid, } from '@material-ui/core';
import Controls from "../../applications/controls/Controls";
import { useForm, Form } from './useForm';
import axios from 'axios'
import {mcq} from './data'

export default function ApplicationForm({type, mc}) {

    //   initValues is used for resetting the form
    let initValues = {}
        //   mappedDataArray is an array of the multiple choice questions
    const mappedDataArray = [];
          // mappedDataFR is an array of the free respnse questions
    const mappedDataFR = [];

           //  validates will ensure that every field has a value, cannot submit without answering each question
    const validate = (fieldValues = values) => {
        let temp = { ...errors }
        for (const atr in mc){
            const el = {
                ...mc[atr]
            }
            if (el.id in fieldValues)
            temp[el.id] = fieldValues[el.id].length != 0 ? "" : "This field is required."
        }
            setErrors({
            ...temp
        })
        let r = Object.values(temp).every(x => x == "")
        if (fieldValues == values)
            console.log(r)
            return r
    }


      if (mc){        
          for (const obj in mc) {
              const val = {
                    ...mc[obj]
              }
              initValues[val.id] = ''
            }
            for (const key in mc) {
                const mappedData = {
                        ...mc[key]
                };

                if (mappedData.type === 'mc'){
                    mappedDataArray.push(mappedData);
            }}

            for (const q in mc) {
                const q_fr = {
                        ...mc[q]
                };

                if (q_fr.type === 'fr'){
                    mappedDataFR.push(q_fr);
                }}
        }
        else{
            console.log('no mc')
        }
        
    // useForm hook
    const {
        values,
        setValues,
        errors,
        setErrors,
        handleInputChange,
        resetForm
    } = useForm(initValues, true, validate);
    

    
    // post form to database
    const handleSubmit = e => {
        e.preventDefault()
        console.log('submit')
        try{
            if (validate()){
                console.log(values)
                const response = fetch('/main/question_set/' + type + '/answer_new', {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(values),
                })
                resetForm()
            }
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <Form onSubmit={handleSubmit}>
            <Grid container>
                <Grid item xs={8}>
                    {mappedDataFR
                    .map(fr_questions => (
                        <Controls.Input
                        key = {fr_questions.id}
                        name={fr_questions.id}
                        label={fr_questions.question}
                        value={values[fr_questions.id]}
                        onChange={handleInputChange}
                        error={errors[fr_questions.id]}
                        />
                    ))
                    }
                    {mappedDataArray
                    .map(multC_questions => (
                        <Controls.Select
                        key = {multC_questions.id}
                        name={multC_questions.id}
                        label={multC_questions.question}
                        value={values[multC_questions.id]}
                        onChange={handleInputChange}
                        options={multC_questions.answers}
                        error={errors[multC_questions.id]}
                    />
                ))}
                    <div>
                        <Controls.Button
                            type="submit"
                            text="Submit" />
                        <Controls.Button
                            text="Reset"
                            color="default"
                            onClick={resetForm} />
                    </div>
                </Grid>
            </Grid>
        </Form>
    )
}
