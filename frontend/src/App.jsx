import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Alarm from "./pages/Alarm";
import Profile from "./pages/Profile";
import Challenge from "./pages/Challenge";

function App(){

 const token = localStorage.getItem("token");
 

 return (

 <Routes>

 <Route path="/" element={<Login/>}/>

 <Route path="/signup" element={<Signup/>}/>


 <Route
 path="/dashboard"
 element={
 token ?
 <>
 <Navbar/>
 <Dashboard/>
 </>
 :
 <Navigate to="/"/>
 }
 />


 <Route
 path="/alarm"
 element={
 token ?
 <>
 <Navbar/>
 <Alarm/>
 </>
 :
 <Navigate to="/"/>
 }
 />


 <Route
 path="/challenge"
 element={
 token ?
 <>
 <Navbar/>
 <Challenge/>
 </>
 :
 <Navigate to="/"/>
 }
 />


 <Route
 path="/profile"
 element={
 token ?
 <>
 <Navbar/>
 <Profile/>
 </>
 :
 <Navigate to="/"/>
 }
 />

 </Routes>

 )

}

export default App;