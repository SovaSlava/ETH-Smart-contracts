/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* global getAssetRegistry getFactory emit */

/**
 * Rent place in big shop
 * @param {org.bigshop.Rent} tx rent
 * @transaction
 */
async function Rent(tx) {  // eslint-disable-line no-unused-vars
	tx.Place.rentUntil = tx.RentUntil;
  	tx.Place.rentBy = tx.RentBy;
    const assetRegistry = await getAssetRegistry('org.bigshop.ShopPlace');
    await assetRegistry.update(tx.Place);

    // Emit an event for the modified asset.
    let event = getFactory().newEvent('org.bigshop', 'RentEvent');
    event.Place = tx.Place;
    event.RentBy = tx.RentBy;
  	event.RentUntil = tx.RentUntil;
    emit(event);
}

/**
 * Rent place in big shop
 * @param {org.bigshop.UnRent} tx rent
 * @transaction
 */
async function UnRent(tx) {  // eslint-disable-line no-unused-vars
	tx.Place.rentUntil = 0;
  	//tx.Place.rentBy = "resource:";
    const assetRegistry = await getAssetRegistry('org.bigshop.ShopPlace');
    await assetRegistry.update(tx.Place);

    // Emit an event for the modified asset.
    let event = getFactory().newEvent('org.bigshop', 'UnRentEvent');
    event.Place = tx.Place;
    emit(event);
}
