import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SegmentedSlider from './SegmentedSlider'
import TrueSlider from './TrueSlider'
import LongTextInput from './LongTextInput'
import axios from 'axios';



function App() {
  const [count, setCount] = useState(0)
  const [mod, setMod] = useState(0)
  const [selectedOccupants, updateOccupants] = useState(1)
  const occupantList = [1,2,3,4]
  const [selectedBathroom, updateBathroom] = useState("Community Bathroom")
  const [selectedBudget, updateBudget] = useState(10000)
  const [accommodation, setAccommodation] = useState("")

  const [top3, setTop3] = useState(null)
  const [top10, setTop10] = useState(null)

  const handleOccupantChange = (event) => {
    updateOccupants(event.target.value)
  }
  const handleBathroomChange = (event) => {
    updateBathroom(event.target.value)
  }
  const handleBudgetChange = (e) => {
    let currVal = e.target.value;

    // If input is empty, set state to an empty string
    if (currVal === "0") {
      updateBudget("");
      e.target.value = ""
    } 
    // Otherwise, parse the number
    else if (!isNaN(currVal)) {
      let newValue = Number(e.target.value);
        if (newValue >= 0 && newValue <= 1000000){
            updateBudget(newValue);
        }
    }
    
  }

  const API_URL = import.meta.env.VITE_API_LINK;
  const handleSubmit = async (e) => {
    e.preventDefault();
    
  
    try {
      let response = await axios.post(
        API_URL + '/ut-prediction', 
        {
          params: {
            occupants: selectedOccupants,
            bathroom: selectedBathroom,
            budget: selectedBudget,
            accommodation: accommodation
          },
          
          
            headers: {
              "Content-Type": "application/json",
            },
            withCredentials: false, // ✅ Avoids sending unnecessary credentials
          }
        
      );
  
      console.log("API Response:", response.data);
      setTop3(response.data.top3);
      setTop10(response.data.top10);
    } catch (error) {
      console.error("Error sending data to API:", error);
    }
  };
  
  
  
  return (
    <>
      <div style = {{flex:1, display: "flex", flexDirection: "column"
      }}>

        
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </button>
          
          <button onClick={() => setCount(count + 1)}>Clicked {count} times</button>
          
        </div>
          <div style = {{display:"flex", justifyContent:"center", alignItems:"center"}}>
            {/* Left Side */}
            <div style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
            }}>
              <div>
                <div>
                  <div style={{ display: "flex", justifyContent: "center", alignItems:"center", marginTop: "0px"}}>
                    Number of Occupants
                  </div>
                  <SegmentedSlider value = {selectedOccupants} setValue = {updateOccupants}/>
                </div>
                
              </div>
              <div>
                <label htmlFor="dropdown">Type of Bathroom</label>
                <select id = "dropdown" value = {selectedBathroom} onChange = {handleBathroomChange} 
                  style = {{marginLeft:"10px"}}>
                  <option value = "Community Bathroom">Community Bathroom</option>
                  <option value = "One Private">One Private</option>
                  <option value = "One Connecting">One Connecting</option>
                  <option value = "Two Private">Two Private</option>
                </select>
              </div>
              <div>
                  <div style={{ display: "flex", justifyContent: "center", alignItems:"center", marginTop: "10px"}}>
                    Budget
                    <input
                    type = "text"
                    value = {selectedBudget}
                    onChange = {handleBudgetChange}
                    
                    style={{
                      
                      marginLeft: "10px",
                      textAlign: "center",
                      background: "white",
                      border: "1px solid gray",
                      borderRadius: "4px",
                      fontSize: "14px",
                      color:"black",
                      
                      
                    }}
                    />
                  </div>
                  
              </div>
            </div>
            {/* Right Side */}
            <div style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
            }}>
              <div>
                <LongTextInput text = {accommodation} setText = {setAccommodation}/>
              </div>
            </div>
        </div>

        {/* Match Me Button */}
        <button 
        onClick = {handleSubmit}
        style = {{
          minWidth:"10px"
        }}>
           - match me! -
        </button>
      </div>
      
    </>
  )
}

export default App
