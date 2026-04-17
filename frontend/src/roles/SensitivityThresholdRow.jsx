import styles from "./sensitivity_threshold_row.module.css"
import { Slider } from 'primereact/slider';
import { InputText } from "primereact/inputtext";

function SensitivityThresholdRow({subcategory, value, setInputValue, setSliderValue}){
    return (
        <div>
            <span>{subcategory}</span>
            <div>
                <Slider value={value} onChange={setSliderValue} min={0} max={50}/> 
                <InputText value={value} onChange={setInputValue} min={0} max={50} type="number"/>
            </div>     
        </div>
    )
}

export default SensitivityThresholdRow;