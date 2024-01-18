import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { createSetting } from '../api/digicore.api';

const Popup = ({ closePopup }) => {
  return (
    <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-black p-8 rounded-md shadow-md text-white">
      <h3 className="text-2xl font-bold mb-4">Instrucciones</h3>
      <p className="mb-4">1. Para denegar internet a un computador (host), escriba: <strong>Denegar el acceso de (nombre del computador) a internet</strong></p>
      <p className="mb-4">2. Para crear una red vlan, escriba: <strong>Crear vlan (nombre de la vlan) en el piso (ubicacion de la vlan)</strong></p>
      <div className="flex justify-center items-end mt-8">
        <button onClick={closePopup} className="bg-violet-500 hover:bg-violet-700 text-white p-3 rounded-md">Cerrar</button>
      </div>
    </div>
  );
};

export function SettingsPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [customError, setCustomError] = useState('');
  const [showPopup, setShowPopup] = useState(false);

  const onSubmit = handleSubmit(async (data) => {
    const re = /(?:Denegar\s+el\s+acceso\s+de\s+(PC1|A|PC2|B|PC3|C|PC4|D)\s+a\s+internet)|(?:Crear\s+vlan\s+(\w+)\s+en\s+el\s+piso\s+(uno|dos))/;
    if (re.test(data.input)) {
      const res = await createSetting(data);
      console.log(res.data['message']);
      if (res.data['message'] === 'Command not found') {
        setCustomError('El lenguaje utilizado no cumple con lo establecido en instrucciones.');
      }else if(res.data['message'] === "Error"){
        setCustomError('El nombre de la vlan ya existe por favor usa otro.');
      } 
      else {
        setCustomError('');
      }
    } else {
      setCustomError('El lenguaje utilizado no cumple con lo establecido en instrucciones.');
    }
  });

  const openPopup = () => {
    setShowPopup(true);
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  return (
    <div className="max-w-xl mx-auto my-auto mt-28">
      <form onSubmit={onSubmit} className="text-center flex flex-col items-center">
        <h2 className="font-bold text-4xl mb-4">Generador de Comandos</h2>
        <textarea
          placeholder="Ingrese su intención"
          cols="70"
          rows="10"
          {...register("input", { required: true })}
          className="bg-zinc-700 p-3 rounded-lg block w-full h-50 mb-3"
        ></textarea>
        {errors.input && (<span className="text-red-100 bg-red-500 text-sm font-bold py-1 px-2 rounded">Este campo es requerido</span>)}
        {customError && (<span className="text-red-100 bg-red-500 text-sm font-bold py-1 px-2 rounded">{customError}</span>)}

        <div className="flex w-full justify-between mt-3">
          <button type="submit" className="bg-violet-500 hover:bg-violet-700 p-3 rounded-lg flex-1">Enviar</button>
          <span onClick={openPopup} className="bg-violet-500 hover:bg-violet-700 p-3 rounded-lg flex-1 ml-2 cursor-pointer">Instrucciones</span>
        </div>
      </form>

      {showPopup && <Popup closePopup={closePopup} />}
    </div>
  );
}
