import logo from './logo.svg';
import placeholder from './Placeholder.jpg'
import {useReducer} from 'react';

interface State {
    count: number 
    
 };

const initialState: State = { count: 0 };



const Register: React.FunctionComponent = () => {
    let likes = 0;
    // const [state, dispatch] = useReducer(useReducer, initialState);
    // const addFive = () => dispatch({ type: "setCount", value: state.count + 5 });
    return (
    
      <div className="App">
        
        <div>
          
          <header className="App-header">
          
            <button>
                Generate RSA 2048 Public/Private Keypair
            </button>
            <button>
                Public Key
            </button>
            <button>
                Private Key
            </button>
            <p>Register</p>
            <input type='text' placeholder='Username'></input>
            <input type='text' placeholder='Public Key'></input>
            <input type='text' placeholder='Profile Picture Url'></input>
            <button id='LoginButtion'>
                Complete Registration 
            </button>
            <button id='Login'>
                Go to Login 
            </button>

            
          </header>
  
  
          
        </div>
      </div>
    );
}

export default Register;
