import React from "react";
import {DefaultLayout} from "@components/shared/DefaultLayout";
import {Home} from "@components/home/Home";

const App = () => {
    return (
    <DefaultLayout>
        <Home/>
    </DefaultLayout>
    );
};

export default App;
