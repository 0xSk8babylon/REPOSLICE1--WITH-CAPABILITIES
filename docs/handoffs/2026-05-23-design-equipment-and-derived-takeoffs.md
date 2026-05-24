# 2026-05-23 Design Equipment And Derived Takeoffs

## What Changed

- Added `DesignEquipment` CRUD routes under `/api/designs/{design_id}/equipment`.
- Added frontend product-assignment workflows inside the System Design Builder.
- Changed `/api/takeoffs/generate/{design_id}` to derive line items from persisted design composition.

## What Is Now True

- Products, quantities, roles, and locations can be assigned directly to each design.
- The takeoff page for a selected design now reflects current design composition instead of the seeded placeholder request.
- Pricing is still placeholder-only and should not be presented as verified estimate data.

## Next Recommended Step

- Add clearer verified-versus-placeholder labels in the product library, design composition, and takeoff views.
- Decide whether generated takeoffs should be stored as versioned records tied to design changes.
